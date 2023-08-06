from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow import DAG
from typing import Callable


class PythonTask(object):
    def __init__(self, dag: DAG, dag_id: str, task_id: str, python_callable: Callable, **kwargs):
        # Python task attributes
        self.dag = dag
        self.task_id = task_id
        self.dag_id = dag_id
        self.python_callable = python_callable
        self._kwargs = kwargs

    def __call__(self) -> Callable:
        return PythonOperator(
            dag=self.dag,
            task_id=self.task_id,
            start_date=datetime(2021, 1, 1),
            python_callable=self.python_callable,
            provide_context=True,
            op_kwargs={
                **self._kwargs,
                "task_id": self.task_id,
                "dag_id": self.dag_id
            }
        )