from pathlib import Path
import docker
import tomli
import json
import os


def build_images_from_operators_repository(
    operators_repository: str = None,
    publish: bool = False
):
    client = docker.from_env()

    if operators_repository is None:
        operators_repository = Path(".")

    dependencies_path = Path(operators_repository) / "dependencies"
    flowui_path = Path(operators_repository) / ".flowui"

    dockerhub_registry_name = "local"
    if publish:
        config_path = Path(operators_repository) / "config.toml"
        with open(config_path, "rb") as f:
            config_dict = tomli.load(f)
        dockerhub_registry_name = config_dict.get("dockerhub").get("REGISTRY_NAME")

    cwd = Path.cwd()
    operators_repository_absolute = Path(operators_repository).resolve()
    operators_repository_ctx_relative = Path(os.path.relpath(operators_repository_absolute, cwd))

    # Load dependencies_map.json file
    with open(flowui_path / "dependencies_map.json", "r") as f:
        operators_dependencies_map = json.load(f)

    # Build docker images from unique definitions
    for k, v in operators_dependencies_map.items():

        dependency_docker_image = v["dependency"].get("docker_image", None)
        dependency_dockerfile = v["dependency"].get("dockerfile", None)
        dependency_requirements = v["dependency"].get("requirements_file", None)

        # If no extra dependency, use base worker image
        if not any([dependency_docker_image, dependency_dockerfile, dependency_requirements]):
            operators_dependencies_map[k]["source_image"] = "taufferconsulting/flowui-airflow-base-worker"
            continue

        # If dependency is defined as an already existing docker image
        elif dependency_docker_image:
            operators_dependencies_map[k]["source_image"] = dependency_docker_image
            continue

        # If dependency is defined as a Dockerfile
        elif dependency_dockerfile:
            source_image_name = f"{dockerhub_registry_name}/{k}"
            operators_dependencies_map[k]["source_image"] = source_image_name
            build_dockerfile_name = dependency_dockerfile
            build_dockerfile_path = str(dependencies_path.resolve())

        # If dependency is defined as a requirements.txt
        elif dependency_requirements:
            source_image_name = f"{dockerhub_registry_name}/{k}"
            operators_dependencies_map[k]["source_image"] = source_image_name
            requirements_file = dependency_requirements
            dockerfile_str = f"""FROM "apache/airflow:2.3.3-python3.8"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER airflow
COPY {Path('dependencies') / requirements_file} .
RUN pip install --user virtualenv \
    && virtualenv flowui_env --system-site-packages\
    && source flowui_env/bin/activate \
    # && /opt/airflow/flowui_env/bin/pip install --upgrade pip \
    && pip install --no-cache-dir -r {requirements_file}
""" 
            build_dockerfile_path = operators_repository_ctx_relative
            build_dockerfile_name = "Dockerfile-tmp"
            full_dockerfile_path = build_dockerfile_path / build_dockerfile_name
            with open(str(full_dockerfile_path), "w") as f:
                f.write(dockerfile_str)
            
        try:
            print(f"Building docker image: {k}")
            img = client.images.build(
                path=str(build_dockerfile_path),
                dockerfile=build_dockerfile_name,
                tag=source_image_name,
                rm=True
            )
            print(f"Finished building: {k}")
            if publish:
                print(f"Publishing docker image: {k}")
                client.login(
                    username=os.getenv("DOCKERHUB_USERNAME"),
                    password=os.getenv("DOCKERHUB_PASSWORD")
                )
                client.images.push(repository=source_image_name)
                print(f"Finished publishing: {k}")
        except Exception as e:
            raise Exception(e)
        finally:
            # remove tmp dockerfile
            if dependency_requirements:
                full_dockerfile_path.unlink()    
    
    return operators_dependencies_map