from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from docker.types import Mount
from datetime import datetime
from typing import Callable
from pathlib import Path
import json
import os

from flowui.operators.python_operator import PythonOperator
from flowui.operators.bash_operator import BashOperator
from flowui.schemas.from_upstream import FromUpstream
from flowui.logger import get_configured_logger


class Task(object):

    def __init__(self, dag: DAG, **kwargs) -> None:
        # Task configuration and attributes
        self.dag = dag
        self.dag_id = kwargs.pop('dag_id')
        self.task_id = kwargs.pop('task_id')
        self.operator_name = kwargs.pop('operator')
        self.deploy_mode = kwargs.pop('deploy_mode')

        # Logger
        self.logger = get_configured_logger(f"{self.__class__.__name__ }-{self.task_id}")

        # Set up Airflow operator using custom function
        self._task_operator = self._set_operator(**kwargs)


    def _set_operator(self, **kwargs) -> None:
        """
        Set airflow operator based on task configuration
        """
        dependencies_map_path = Path(os.getenv("VOLUME_MOUNT_PATH_DOCKER")) / "code_repository/.flowui/dependencies_map.json"
        with open(dependencies_map_path, "r") as f:
            dependencies_map = json.load(f)
        dependencies_group = [k for k, v in dependencies_map.items() if self.operator_name in v["operators"]][0]

        if self.deploy_mode == "local-python":
            return PythonOperator(
                dag=self.dag,
                task_id=self.task_id,
                start_date=datetime(2021, 1, 1), # TODO - get correct start_date
                provide_context=True,
                op_kwargs=kwargs,
                queue=dependencies_group,
                make_python_callable_kwargs=dict(
                    operator_name=self.operator_name,
                    deploy_mode=self.deploy_mode,
                    task_id=self.task_id,
                    dag_id=self.dag_id,
                )
            )
        
        elif self.deploy_mode == "local-bash":
            cmds = 'source /opt/airflow/flowui_env/bin/activate && pip install -e /opt/flowui && flowui run-operator-bash'
            return BashOperator(
                dag=self.dag,
                task_id=self.task_id,
                queue=dependencies_group,
                bash_command=cmds,
                env={
                    "FLOWUI_BASHOPERATOR_OPERATOR_NAME": self.operator_name,
                    "FLOWUI_BASHOPERATOR_INSTANTIATE_OP_KWARGS": str({
                        "deploy_mode": self.deploy_mode,
                        "task_id": self.task_id,
                        "dag_id": self.dag_id,
                    }),
                    "FLOWUI_BASHOPERATOR_RUN_OP_KWARGS": str(kwargs),
                },
                append_env=True
            )
        
        elif self.deploy_mode == "local-docker":
            # Get Docker image for this Operator, from dependencies_map.json
            volume_mount_path = os.getenv("VOLUME_MOUNT_PATH_DOCKER", "/opt/airflow/mnt/fs")
            dependencies_map_path = Path(volume_mount_path) / f"code_repository/dependencies/dependencies_map.json"
            with open(dependencies_map_path, "r") as f:
                dependencies_map = json.load(f)
            for k, v in dependencies_map.items():
                if self.operator_name in v["operators"]:
                    docker_image_name = k
                    continue

            # Container ENV variables
            container_env_vars = {
                "FLOWUI_K8S_EXECUTION_ENV_VARS": {
                    "FLOWUI_K8S_OPERATOR_NAME": self.operator_name,
                    "FLOWUI_K8S_INIT_OPERATOR_VARS": {
                        "deploy_mode": self.deploy_mode,
                        "task_id": self.task_id,
                        "dag_id": self.dag_id,
                    },
                    "FLOWUI_K8S_RUN_OPERATOR_VARS": kwargs,
                    "VOLUME_MOUNT_PATH": volume_mount_path
                }
            }
            
            # Command to run
            # script_to_run = "from flowui.k8s_run_operator import run_operator; run_operator()"
            # cmds = ["pip", "install", "-e", "./flowui", "&&", "python", "-c", script_to_run]
            cmds = "/bin/bash -c 'pip install -e ./flowui && flowui run-operator-docker'"

            # Volume mounts
            source_mnt_path = os.getenv("VOLUME_MOUNT_PATH_HOST", "mnt/fs")
            volume_mounts = [
                # Mount(target=volume_mount_path, source=source_mnt_path),
                # Mount(target="/var/run/docker.sock", source="/var/run/docker.sock", type="bind")
                Mount(target="/mnt/fs", source="/media/luiz/storage/Github/flowui/mnt/fs", type="bind"),
                Mount(target="/flowui", source="/media/luiz/storage/Github/flowui/flowui", type="bind"),
            ]

            return DockerOperator(
                dag=self.dag,
                task_id=self.task_id,
                image=docker_image_name,
                environment=container_env_vars,
                command=cmds,
                mounts=volume_mounts,
                # docker_url="unix://var/run/docker.sock",
                docker_url='tcp://docker-proxy:2375',
                network_mode="bridge",
                xcom_all=True,
                mount_tmp_dir=False,
                privileged=True
            )

        elif self.deploy_mode == "kubernetes":
            # TODO
            script_to_run = "/bin/bash -c 'flowui run-operator-docker'"
            cmds = ["python", "-c", script_to_run]
            # TODO - pass relevant airflow context information:
            # https://groups.google.com/g/cloud-composer-discuss/c/fqAsq35enJ0/m/bhMau7XSAwAJ
            container_env_vars = {
                "FLOWUI_K8S_EXECUTION_ENV_VARS": {
                    "FLOWUI_K8S_OPERATOR_NAME": self.operator_name,
                    "FLOWUI_K8S_INIT_OPERATOR_VARS": {
                        "deploy_mode": self.deploy_mode,
                        "task_id": self.task_id,
                        "dag_id": self.dag_id,
                    },
                    "FLOWUI_K8S_RUN_OPERATOR_VARS": kwargs
                }
            }
            return KubernetesPodOperator(
                # namespace='default',
                # image="ubuntu:16.04",
                task_id=self.task_id,
                cmds=cmds,
                # arguments=["echo", "10"],
                env_vars=container_env_vars,
                do_xcom_push=True,
                # labels={"foo": "bar"},
                # secrets=[secret_file, secret_env, secret_all_keys],
                # ports=[port],
                # volumes=[volume],
                # volume_mounts=[volume_mount],
                # env_from=configmaps,
                # name="airflow-test-pod",
                # affinity=affinity,
                # is_delete_operator_pod=True,
                # hostnetwork=False,
                # tolerations=tolerations,
                # init_containers=[init_container],
                # priority_class_name="medium",
            )

    def __call__(self) -> Callable:
        return self._task_operator