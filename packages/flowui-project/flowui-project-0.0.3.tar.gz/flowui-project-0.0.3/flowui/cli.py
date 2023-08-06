from pathlib import Path
from python_on_whales import DockerClient
from jsonschema import validate
import collections.abc
import uuid
import os
import re
import argparse
import json
import subprocess
import copy
import tomli
import tomli_w
import shutil

from flowui.scripts.build_docker_images_operators import build_images_from_operators_repository
from flowui.scripts.create_docker_compose_file import create_docker_compose_file
from flowui.scripts.run_operator_docker import run_operator as run_operator_in_docker
from flowui.scripts.run_operator_bash import run_operator as run_operator_in_bash
from flowui.scripts.load_operator import load_operator_models_from_path
from flowui.schemas.operator_metadata import OperatorMetadata
from flowui.utils.metadata_default import metadata_default
from flowui.logger import get_configured_logger
from typing import Union


def dict_deep_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = dict_deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


class CommandLineInterface:

    def __init__(self):
        self.logger = get_configured_logger(self.__class__.__name__)
        self.config_required_fields = {
            "REPOSITORY_NAME": None,
            "FLOWUI_DEPLOY_MODE": None,
            "VOLUME_MOUNT_PATH_HOST": None,
            "OPERATORS_REPOSITORY_SOURCE": None,
            "GITHUB_REPOSITORY_NAME": None,
        }

        self.required_env_vars_validators = {
            "GITHUB_ACCESS_TOKEN": {
                "depends": lambda arg: arg.get('OPERATORS_REPOSITORY_SOURCE') == 'github',
                "validator_func": self._validate_github_token
            }
        }
        self.args = self._parse_arguments()
    

    @staticmethod
    def _parse_arguments() -> argparse.Namespace:
        """Parse user CLI arguments and actions

        The accepted actions are:
            - organize: Organize the Operators repository into a FlowUI structure.
            - run: Create docker-compose file and run the FlowUI platform locally.
            - run-local-dev: Create docker-compose file and run the FlowUI platform locally in development mode.
            - stop: Stop the FlowUI platform.
            - create-compose-file: Create a docker-compose file for the FlowUI platform.
            - run-operator-docker: Run an operator using docker.
            - run-operator-bash: Run an operator using bash.

        The accepted arguments are:
            - operators_repository_path: Path to the Operators repository

        Returns:
            argparse.Namespace: Parsed arguments
        """
        parser = argparse.ArgumentParser(
            description='CLI for FlowUI',
        )

        action_choices = [
            'organize', 
            'run', 
            'stop', 
            'create-compose-file', 
            'run-local-dev', 
            'run-operator-docker', 
            'run-operator-bash', 
            'create-operators-repository'
        ]
        parser.add_argument(
            'action', 
            metavar='Action', 
            type=str, 
            choices=action_choices,
            help=f'action to be executed: {" | ".join(action_choices)}'
        )

        parser.add_argument(
            "--operators_repository_path",
            type=str,
            default="./",
            help="Path to Operators repository"
        )

        parser.add_argument(
            "--build-images",
            action='store_true',
            help="Build Docker images"
        )

        parser.add_argument(
            "--publish-images",
            action='store_true',
            help="Publish Docker images to Docker Hub"
        )

        args = parser.parse_args()

        return args
    

    def run(self) -> None:
        """
        Run FlowUI using local deploy scope.
        This will create a docker-compose.yaml file and run it.
        """
        self._validate_repository_structure()
        self._create_mnt_required_folders()
        self.create_docker_compose_file()
        self.docker = DockerClient(compose_files=["docker-compose.yaml"])
        self.docker.compose.up()


    def run_local_dev(self) -> None:
        """
        Run FlowUI using local development environment scope.
        This will create a docker-compose.yaml file and run it.
        """ 
        self._validate_repository_structure()
        if not os.environ.get('FLOWUI_PATH_HOST'):
            os.environ['FLOWUI_PATH_HOST'] = str(Path('../flowui').resolve())
        self._create_mnt_required_folders()
        self.create_docker_compose_file(run_scope="local-dev")
        self.docker = DockerClient(compose_files=["docker-compose.yaml"])
        self.docker.compose.up()


    def stop_compose(self) -> None:
        """Stop FlowUI. From the running docker compose, stop and remove the running containers"""
        compose = Path("docker-compose.yaml")
        if not compose.is_file():
            raise Exception("docker-compose.yaml file not found")
        try:
            self.logger.info("Stopping docker-compose...")
            self.docker = DockerClient(compose_files=["docker-compose.yaml"])
            self.docker.compose.down()
        except Exception as e: # work on python 3.x
            self.logger.info('Failed to stop compose processes: '+ str(e))
        # TODO - add docker stop and docker rm


    def _validate_repository_structure(self) -> None:
        """
        Validate the Operators repository structure.
        The basic structure must contain:
        - config.toml
        - operators/
        - dependencies/
        """
        self.operators_path = Path(self.args.operators_repository_path) / "operators"
        self.dependencies_path = Path(self.args.operators_repository_path) / "dependencies"
        self.organized_flowui_path = Path(self.args.operators_repository_path) / ".flowui/"
        if not self.organized_flowui_path.is_dir():
            self.organized_flowui_path.mkdir(parents=True, exist_ok=True)
        
        # Validating config
        self.config_path = Path(self.args.operators_repository_path) / 'config.toml'
        if not self.config_path.is_file():
            self.logger.error("Missing config file")
            raise FileNotFoundError("Missing config file")

        with open(self.config_path, "rb") as f:
            self.config_dict = tomli.load(f)

        self._validate_config()
        self._validate_env_vars()

        operators_repository = Path(self.args.operators_repository_path)
        if not operators_repository.is_dir():
            self.logger.error("Operators repository path does not exist")
            raise Exception("Operators repository path does not exist")

        if not (operators_repository / 'config.toml').is_file():
            self.logger.error("config.toml file does not exist")
            raise Exception("config.toml file does not exist")

        if not (operators_repository / 'operators').is_dir():
            self.logger.error("Operators directory does not exist")
            raise Exception("Operators directory does not exist")
        
        if not (operators_repository / 'dependencies').is_dir():
            self.logger.error("Dependencies directory does not exist")
            raise Exception("Dependencies directory does not exist")
        os.environ['OPERATORS_REPOSITORY_PATH_HOST'] = str(operators_repository)


    def _validate_config(self) -> None:
        """
        Validate user config.toml file and save it to config_dict and as environment variables to be used by the docker-compose file
        """
        required_fields = list(self.config_required_fields.keys()).copy()
        required_secrets = list()
        sections = self.config_dict.keys()
        for section in sections:
            for key, value in self.config_dict.get(section).items():
                # Check if OPERATORS_SECRETS exist in environment
                if section == "repository" and key == "OPERATORS_SECRETS":
                    for v in value:
                        if not os.getenv(v, None):
                            required_secrets.append(v)
                # Check if required fields were defined in config file
                elif key in self.config_required_fields:
                    required_fields.remove(key.upper())
                    if key in ["VOLUME_MOUNT_PATH_HOST", "FLOWUI_PATH_HOST"]:
                        value = str(Path(value).resolve())
                    # Set config as env vars, it will be used by compose
                    self._set_config_as_env(key, value) 
                    self.config_required_fields[key.upper()] = value

        if len(required_fields) > 0:
            self.logger.error("Missing required fields: {}".format(required_fields)) 
        if len(required_secrets) > 0:
            missing = '\n'.join(required_secrets)
            self.logger.warning(f"Missing required operators secrets. These shold be defined in your ENV: \n{missing}") 


    def _validate_env_vars(self) -> None:
        """
        Validate user environment variables.
        The accepted variables are:
            - GITHUB_ACCESS_TOKEN: Token to access GitHub API.
        """
        # Set AIRFLOW_UID from host user id 
        # https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html#setting-the-right-airflow-user
        # https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html#environment-variables-supported-by-docker-compose
        uid = subprocess.run(["id", "-u"], capture_output=True, text=True)
        self._set_config_as_env("AIRFLOW_UID", int(uid.stdout)) 

        for var, validator in self.required_env_vars_validators.items():
            if 'depends' in validator:
                should_exists = validator.get('depends')(self.config_required_fields)
            if not should_exists:
                continue
            env_var = os.environ.get(var, None)
            if env_var:
                continue
            self.logger.warning(f"{var} is not defined")
            new_var = input(f"Enter the {var} value: ")
            while not validator.get('validator_func')(new_var):
                new_var = input(f"Wrong {var} format. Enter a new value: ")
            os.environ[var] = new_var


    @staticmethod
    def _set_config_as_env(key: Union[str, int], value: Union[str, int, float]):
        """
        Set an ENV variable with the key and value.

        Args:
            key (Union[str, int]): ENV var name
            value (Union[str, int, float]): ENV var value
        """
        key = str(key).strip().upper()
        os.environ[key] = str(value)


    @staticmethod
    def _validate_github_token(token: str) -> bool:
        """
        Validate GITHUB_ACCESS_TOKEN
        By now it is only accepting the ghp token.

        Args:
            token (str): Github access token (ghp)

        Returns:
            bool: True if token is valid, False otherwise.
        """
        regex = r"ghp_[0-9a-zA-Z]{35,40}"
        pattern = re.compile(regex)
        if pattern.match(token):
            return True
        return False


    def _validate_operators_repository(self) -> None:
        """
        Validate the Operators repository structure.
        """
        dependencies_files = [f.name for f in self.dependencies_path.glob("*")]
        name_errors = list()
        missing_file_errors = list()
        missing_dependencies_errors = list()
        for op_dir in self.operators_path.glob("*Operator"):
            if op_dir.is_dir():
                # Validate necessary files exist
                files_names = [f.name for f in op_dir.glob("*")]
                if 'models.py' not in files_names:
                    missing_file_errors.append(f"missing 'models.py' for {op_dir.name}")
                if 'operator.py' not in files_names:
                    missing_file_errors.append(f"missing 'operator.py' for {op_dir.name}")
                if len(missing_file_errors) > 0:
                    raise Exception('\n'.join(missing_file_errors))

                # Validate metadata
                if (op_dir / "metadata.json").is_file():
                    with open(str(op_dir / "metadata.json"), "r") as f:
                        metadata = json.load(f)
                    validate(instance=metadata, schema=OperatorMetadata.schema())

                    # Validate Operators name
                    if metadata.get("name", None) and not metadata["name"] == op_dir.name:
                        name_errors.append(op_dir.name)
                    
                    # Validate dependencies exist
                    if metadata.get("dependency", None):
                        req_file = metadata["dependency"].get("requirements_file", None)
                        if req_file and req_file != "default" and req_file not in dependencies_files:
                            missing_dependencies_errors.append(f'missing dependency file {req_file} defined for {op_dir.name}')
                        
                        dock_file = metadata["dependency"].get("dockerfile", None)
                        if dock_file and dock_file != "default" and dock_file not in dependencies_files:
                            missing_dependencies_errors.append(f'missing dependency file {dock_file} defined for {op_dir.name}')
    
        if len(name_errors) > 0:
            raise Exception(f"The following Operators have inconsistent names: {', '.join(name_errors)}")
        if len(missing_dependencies_errors) > 0:
            raise Exception("\n" + "\n".join(missing_dependencies_errors))


    def _build_docker_images(self) -> None:
        """Convenience function to build Docker images from the repository dependencies and publish them to Docker Hub"""
        self.logger.info("Building Docker images and generating map file...")
        updated_dependencies_map = build_images_from_operators_repository(
            operators_repository=self.args.operators_repository_path,
            publish=self.args.publish_images
        )
        return updated_dependencies_map


    def create_docker_compose_file(self, run_scope="deploy-local")-> None:
        """
        Convenience function to create docker-compose.yaml file in the operators_repository directory.

        Args:
            run_scope (str): Scope of the run. Default is deploy-local. Options are (deploy-local, local-dev)
        """
        self.logger.info("Creating docker-compose.yaml file...")
        create_docker_compose_file(
            repository_path=self.args.operators_repository_path,
            run_scope=run_scope,
            repository_config=self.config_dict
        )
        self.logger.info("docker-compose.yaml file created successfully!")


    def _create_mnt_required_folders(self):
        """Function to create required folders in user mount path
        Required folders are:
        - airflow
        ----|logs
        ----|plugins
        ----| dags 
        - operators_repository
        --| operators
        --| workflows
        - datasets
        - runs
        - tmp
        """
        self.logger.info("Creating required folders in mount...")

        # Mount folder
        base_path = Path(self.config_required_fields.get("VOLUME_MOUNT_PATH_HOST"))
        if not base_path.exists():
            base_path.mkdir(parents=True, exist_ok=True)

        # Airflow folders
        airflow_path = base_path / "airflow"
        if not airflow_path.exists():
            airflow_path.mkdir(parents=True, exist_ok=True)
        airflow_logs_path = airflow_path / "logs"
        if not airflow_logs_path.exists():
            airflow_logs_path.mkdir(parents=True, exist_ok=True)
        airflow_plugins_path = airflow_path / "plugins"
        if not airflow_plugins_path.exists():
            airflow_plugins_path.mkdir(parents=True, exist_ok=True)
        airflow_dags_path = airflow_path / "dags"
        if not airflow_dags_path.exists():
            airflow_dags_path.mkdir(parents=True, exist_ok=True)

        # Operators repository folders
        operators_repository_path = base_path / "operators_repository"
        if not operators_repository_path.exists():
            operators_repository_path.mkdir(parents=True, exist_ok=True)
        operators_repository_operators_path = operators_repository_path / "operators"
        if not operators_repository_operators_path.exists():
            operators_repository_operators_path.mkdir(parents=True, exist_ok=True)
        operators_repository_workflows_path = operators_repository_path / "workflows"
        if not operators_repository_workflows_path.exists():
            operators_repository_workflows_path.mkdir(parents=True, exist_ok=True)

        # Datasets folder
        datasets_path = base_path / "datasets"
        if not datasets_path.exists():
            datasets_path.mkdir(parents=True, exist_ok=True)

        # Runs folder
        runs_path = base_path / "runs"
        if not runs_path.exists():
            runs_path.mkdir(parents=True, exist_ok=True)

        # Temp folder
        tmp_path = base_path / "tmp"
        if not tmp_path.exists():
            tmp_path.mkdir(parents=True, exist_ok=True)
        self.logger.info("Required folders created successfully!")


    def _create_dependencies_map(self, save_map_as_file: bool = True) -> None:
        """
        Construct a map between Operators and unique definitions for docker images dependencies

        Args:
            save_map_as_file (bool, optional): Set if dependencies_map will be saved as file. Defaults to True.

        Raises:
            ValueError: Raise if operators is not found in the operators_repository
        """
        with open(self.organized_flowui_path / "compiled_metadata.json", "r") as f:
            compiled_metadata = json.load(f)
    
        operators_images_map = {}
        for op_i, (operator_name, operator_metadata) in enumerate(compiled_metadata.items()):
            if op_i == 0:
                operators_images_map = {
                    "flowui-dependency-0": {
                        "dependency": operator_metadata["dependency"],
                        "operators": [operator_name]
                    }
                }
            else:
                # Compare with metadata from previous operators to see if a new docker image needs to be built
                existing_keys = operators_images_map.keys()
                skip_new_image = False
                for i, dep_key in enumerate(existing_keys):
                    if all([operator_metadata["dependency"][k] == operators_images_map[dep_key]["dependency"][k] for k in operator_metadata["dependency"].keys()]):
                        operators_images_map[dep_key]["operators"].append(operator_name)
                        skip_new_image = True
                        continue
                if not skip_new_image:
                    operators_images_map[f"flowui-dependency-{len(existing_keys)}"] = {
                        "dependency": operator_metadata["dependency"],
                        "operators": [operator_name]
                    }

        if not operators_images_map:
            raise ValueError("No operators found in the Operators repository")

        if save_map_as_file:
            map_file_path = self.organized_flowui_path / "dependencies_map.json"
            with open(map_file_path, "w") as outfile:
                json.dump(operators_images_map, outfile, indent=4)


    def _create_compiled_operators_metadata(self) -> None:  
        """Create compiled metadata from Operators metadata.json files and include input_schema generated from models.py"""
        compiled_metadata = dict()
        for op_dir in self.operators_path.glob("*Operator"):
            if op_dir.is_dir():
                operator_name = op_dir.name

                # Update with user-defined metadata.json
                metadata = copy.deepcopy(metadata_default)
                if (op_dir / "metadata.json").is_file():
                    with open(str(op_dir / "metadata.json"), "r") as f:
                        metadata_op = json.load(f)
                    dict_deep_update(metadata, metadata_op)
                    metadata["name"] = operator_name

                # Add input and output schemas
                input_model_class, output_model_class, secrets_model_class = load_operator_models_from_path(operators_folder_path=str(self.operators_path), operator_name=op_dir.name)
                metadata["input_schema"] = input_model_class.schema()
                metadata["output_schema"] = output_model_class.schema()
                metadata["secrets_schema"] = secrets_model_class.schema() if secrets_model_class else None

                # Add to compiled metadata
                compiled_metadata[operator_name] = metadata
        
        # Save compiled_metadata.json file
        with open(str(self.organized_flowui_path / "compiled_metadata.json"), "w") as f:
            json.dump(compiled_metadata, f, indent=4)


    def create_operators_repository(self) -> None:
        """
        Create a new Operators repository with folder structure and basic example files:

        1. Create config.toml file
        2. Create operators folder
        3. Create dependencies folder
        4. Create .flowui folder
        5. Create example operators files
        6. Create example dependency files
        7. Run flowui organize
        """
        repository_name = input("Enter the repository's name: ") or f"new-repository-{str(uuid.uuid4())[0:8]}"
        while not self._validate_repository_name(repository_name):
            repository_name = input("\nInvalid repository name. Should have only numbers, letters, underscores and dashes. \nEnter a new repository name: ") or f"new-repository-{str(uuid.uuid4())[0:8]}"
        cwd = Path.cwd()
        repository_folder = cwd / repository_name
        if repository_folder.is_dir():
            raise Exception("Repository folder already exists")
        repository_folder.mkdir()
        self.logger.info(f"Creating repository in {repository_folder}")
        self._create_config_toml(repository_path=repository_folder, repository_name=repository_name)
        self._create_repository_folders(repository_folder)
        subprocess.call(f"cd {str(repository_folder)} && flowui organize", shell=True)


    @staticmethod
    def _validate_repository_name(name: str):
        regex = r'^[A-Za-z0-9_-]*$'
        pattern = re.compile(regex)
        if pattern.match(name):
            return True
        return False


    def _create_config_toml(self, repository_path: Path, repository_name: str) -> None:
        """
        Create Operators repository basic config.toml file

        Args:
            path (Path): _description_
            repository_name (str): _description_
        """
        default_mount_path_host = Path.cwd() / f'{repository_name}/mnt/fs'
        data = {
            "repository": {
                "REPOSITORY_NAME": repository_name,
                "FLOWUI_DEPLOY_MODE": "local-bash",
                "VOLUME_MOUNT_PATH_HOST": str(default_mount_path_host),
                "OPERATORS_SECRETS": [],
                "OPERATORS_REPOSITORY_SOURCE": "local",
                "GITHUB_REPOSITORY_NAME": ""
            } 
        }
        with open(str(repository_path / 'config.toml'), 'wb') as out:
            tomli_w.dump(data, out)


    def _create_repository_folders(self, repository_path: Path) -> None:
        """
        _summary_

        Args:
            repository_path (Path): _description_
        """
        self.logger.info("Creating new repository folders...")
        import flowui.example_repository as example_repository
        example_repository_source_path = Path(os.path.dirname(example_repository.__file__))

        operators_dst_path = repository_path / "operators"
        if not operators_dst_path.is_dir():
            shutil.copytree(str(example_repository_source_path / "operators"), str(operators_dst_path))

        flowui_path = repository_path / ".flowui"
        if not flowui_path.is_dir():
            shutil.copytree(str(example_repository_source_path / ".flowui"), str(flowui_path))

        dependencies_path = repository_path / 'dependencies'
        if not dependencies_path.is_dir():
            shutil.copytree(str(example_repository_source_path / 'dependencies'), str(dependencies_path))
    

    def organize_operators_repository(self) -> None:
        """
        Organize Operator's repository for FlowUI.
        This will validate the folder structure, and create the operators compiled_metadata.json and dependencies_map.json files.
        """        
        # Validate repository
        self._validate_repository_structure()
        self._validate_operators_repository()
        
        # Create compiled metadata from Operators metadata.json files and add data input schema
        self._create_compiled_operators_metadata()
        
        # Generate dependencies_map.json file
        self._create_dependencies_map(save_map_as_file=True)

        # Build and publish the images
        if self.args.build_images:
            updated_dependencies_map = self._build_docker_images()
            map_file_path = self.organized_flowui_path / "dependencies_map.json"
            with open(map_file_path, "w") as outfile:
                json.dump(updated_dependencies_map, outfile, indent=4)


    def run_operator_in_docker(self) -> None:
        """Convenience function to run Operators within Docker images"""
        self.logger.info("Running Operator...")
        run_operator_in_docker()
    

    def run_operator_in_bash(self) -> None:
        """Convenience function to run Operators from a bash script"""
        self.logger.info("Running Operator...")
        run_operator_in_bash()


def cli():
    cli = CommandLineInterface()
    cli_args = cli.args
    cli_func_map = {        
        # Run locally
        "run": cli.run,
        "stop": cli.stop_compose,
        "create-compose-file": cli.create_docker_compose_file,
        "run-local-dev": cli.run_local_dev,
        
        # Operator's repository
        "create-operators-repository": cli.create_operators_repository,
        "organize": cli.organize_operators_repository,
        
        # Run Operator
        "run-operator-docker": cli.run_operator_in_docker,
        "run-operator-bash": cli.run_operator_in_bash,
    }
    cli_func_map[cli_args.action]()
