from airflow.providers.amazon.aws.operators.batch import AwsBatchOperator
import os
import uuid
import numpy as np
from airflow import DAG
from typing import Callable

class AWSBatchTask(object):
    def __init__(self,
        dag: DAG,
        dag_id: str,
        task_id: str,
        operator_name: str,
        operator_version: str,
        **kwargs
    ) -> None:
        # AWS task attributes
        self.dag = dag
        self.dag_id = dag_id
        self.task_id = task_id
        self.operator_name = operator_name
        self.operator_version = operator_version
        self._kwargs = kwargs

    def __call__(self) -> Callable:
        override_command = [
            'python', f'custom_operators/{self.operator_name}/operator_function.py',
        ] + list(np.concatenate([[f"--{k}", v] for k, v in self._kwargs.items()]).flat)
        return AwsBatchOperator(
            dag=self.dag,
            task_id=self._kwargs.get('task_id'),
            job_name=f"{self.operator_name}_{self.operator_version}_{str(uuid.uuid4())}", 
            job_definition=os.environ.get(f"AWS_BATCH_JOB_DEFINITION_{self.operator_name}_{self.operator_version}"),  # 'arn:aws:batch:eu-central-1:XXXX:job-definition/my-job-name'
            job_queue=os.environ.get(f"AWS_BATCH_JOB_QUEUE_{self.operator_name}_{self.operator_version}"),  # 'arn:aws:batch:eu-central-1:XXXX:job-queue/my-job-name'
            region_name=os.environ.get("AWS_REGION_NAME"), 
            overrides={
                'command': override_command,
            }
        )
        
    