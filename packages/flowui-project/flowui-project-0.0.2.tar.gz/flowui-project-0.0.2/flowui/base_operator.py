import abc
import json
import os
import ast
from datetime import datetime
from pathlib import Path

from flowui.client.airflow_client import AirflowRestClient
from flowui.schemas.from_upstream import FromUpstream
from flowui.logger import get_configured_logger
from flowui.utils.enum_types import DeployModeType


class BaseOperator(metaclass=abc.ABCMeta):

    @classmethod
    def set_metadata(cls, metadata):
        """
        _summary_

        Args:
            metadata (_type_): _description_
        """
        # Operator name as used by Airflow
        cls.__name__ = metadata.get("name", "BaseOperator")

        # Operator version: update it to auto update the deployed version
        cls.__version__ = metadata.get("version", "0.1.0")

        # Dockerfile to build Image for this function
        cls.__dockerfile__ = metadata.get("dockerfile", "Dockerfile-base")

        # Full metadata
        cls._metadata_ = metadata


    def __init__(
        self,
        deploy_mode: DeployModeType,
        task_id: str,
        dag_id: str,
    ) -> None:
        """
        The base class from which every FlowUI custom Operator should inherit from.
        BaseOperator methods and variables that can be used by inheriting Operators:

        self._metadata_ - Metadata as defined by the user
        self.upstream_tasks - Metadata and XCom data results from previous Tasks
        self.results_path - Path to store results data
        self.logger - Logger functionality

        Args:
            deploy_mode (DeployModeType): _description_
            task_id (str): _description_
            dag_id (str): _description_
        """

        # Operator task attributes
        self.task_id = task_id
        self.dag_id = dag_id
        self.deploy_mode = deploy_mode

        # Clients
        self.airflow_client = AirflowRestClient()

        # Logger
        self.logger = get_configured_logger(f"{self.__class__.__name__ }-{self.task_id}")


    def generate_paths(self):
        """
        _summary_
        """
        self.volume_mount_path = os.environ.get("VOLUME_MOUNT_PATH_DOCKER", "/opt/mnt/fs")
        self.run_id = str(self.airflow_context['execution_date']).replace(":", "-").replace(".", "").replace("+", "-") 
        
        self.run_path = f"{self.volume_mount_path}/runs/{self.dag_id}/{self.run_id}"
        if not Path(self.run_path).is_dir():
            Path(self.run_path).mkdir(parents=True, exist_ok=True)
        
        self.results_path = f"{self.run_path}/{self.task_id}/results"
        if not Path(self.results_path).is_dir():
            Path(self.results_path).mkdir(parents=True, exist_ok=True)
        
        self.report_path = f"{self.run_path}/{self.task_id}/report"
        if not Path(self.report_path).is_dir():
            Path(self.report_path).mkdir(parents=True, exist_ok=True)


    def get_upstream_tasks(self):
        """
        _summary_

        Raises:
            NotImplementedError: _description_
        """
        self.upstream_task_xcom = dict()
        if self.deploy_mode == "local-python":
            for tid in list(self.airflow_context['task'].upstream_task_ids):
                self.upstream_task_xcom[tid] = self.airflow_context['ti'].xcom_pull(task_ids=tid) 
        elif self.deploy_mode == "local-bash":
            with open("/opt/mnt/fs/tmp/xcom_input.json") as f:
                self.upstream_task_xcom = json.load(f)
        else:
            raise NotImplementedError(f"Get upstream XCOM not implemented for deploy_mode=={self.deploy_mode}")

    def start_logger(self):
        """
        _summary_
        """
        self.logger.info(f"Started {self.task_id} of type {self.__class__.__name__} at {str(datetime.now().isoformat())}")


    def validate_and_format_xcom(self, xcom_obj: dict):
        """
        _summary_

        Args:
            xcom_obj (dict): _description_

        Returns:
            _type_: _description_
        """
        if not isinstance(xcom_obj, dict):
            print(f"Operator {self.__class__.__name__} is not returning a valid XCOM object. Auto-generating a base XCOM for it...")
            self.logger.info(f"Operator {self.__class__.__name__} is not returning a valid XCOM object. Auto-generating a base XCOM for it...")
            xcom_obj = dict()

        xcom_obj.update(
            operator_name=self.__class__.__name__,
            operator_metadata=self._metadata_,
            results_path=self.results_path,
        )
        return xcom_obj


    def push_xcom(self, xcom_obj: dict):
        """
        _summary_

        Args:
            xcom_obj (dict): _description_

        Raises:
            NotImplementedError: _description_
        """
        if self.deploy_mode == "local-python":
            self.airflow_context['ti'].xcom_push(key=self.task_id, value=xcom_obj)
        elif self.deploy_mode == "local-bash":
            # For our extended BashOperator, return XCom must be stored in /opt/mnt/fs/tmp/xcom_output.json
            file_path = Path("/opt/mnt/fs/tmp/xcom_output.json")
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(str(file_path), 'w') as fp:
                json.dump(xcom_obj, fp, indent=4)
        elif self.deploy_mode == "kubernetes":
            # In Kubernetes, return XCom must be stored in /airflow/xcom/return.json
            # https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#how-does-xcom-work
            file_path = Path('/airflow/xcom/return.json')
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(str(file_path), 'w') as fp:
                json.dump(xcom_obj, fp)
        else:
            raise NotImplementedError("deploy mode not accepted for xcom push")
    

    def run_operator_function(self, operator_input_model, operator_output_model, op_kwargs, airflow_context):
        """
        _summary_

        Args:
            operator_input_model (_type_): _description_
            operator_output_model (_type_): _description_
            op_kwargs (_type_): _description_
            airflow_context (_type_): _description_
        """
        # Airflow context dictionary: https://composed.blog/airflow/execute-context
        # For local-bash and kubernetes deploy modes, we assemble this ourselves and the context data is more limited
        self.airflow_context = airflow_context
        self.dag_run_id = airflow_context.get("dag_run_id")

        self.generate_paths()
        self.get_upstream_tasks()
        self.start_logger()

        # Using pydantic to validate input data
        # operator_model_obj = operator_input_model(**op_kwargs)
        updated_op_kwargs = dict()
        for k, v in op_kwargs.items():
            if isinstance(v, dict) and v.get("type") == "FromUpstream":
                upstream_task_id = v.get("upstream_task_id")
                output_arg = v.get("output_arg")
                updated_op_kwargs[k] = self.upstream_task_xcom[upstream_task_id][output_arg]
            else:
                updated_op_kwargs[k] = v
        input_model_obj = operator_input_model(**updated_op_kwargs)

        # # In kubernetes, we get airflow_context from ENV vars
        # if self.deploy_mode == "kubernetes":
        #     # TODO
        #     pass 

        # Run operator function
        output_model_obj = self.operator_function(input_model=input_model_obj)

        # Push XCom
        xcom_obj = self.validate_and_format_xcom(xcom_obj=output_model_obj.dict())
        self.push_xcom(xcom_obj=xcom_obj)


    @abc.abstractmethod
    def operator_function(self):
        """
        This function carries the relevant code for the Operator run
        It should have all the necessary content for auto-generating json schemas
        All arguments should be type annotated and docstring should carry description for each argument.
        """
        raise NotImplementedError("This method must be implemented in the child class!")        


    def generate_report(self):
        """
        This function carries the relevant code for the Operator report
        """
        raise NotImplementedError("This method must be implemented in the child class!")
