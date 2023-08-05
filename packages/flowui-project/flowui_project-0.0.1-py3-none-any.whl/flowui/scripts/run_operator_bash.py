import airflow
from flowui.scripts.load_operator import load_operator_class_from_path, load_operator_models_from_path
from pathlib import Path
import os
import ast
import json


def run_operator():
    # Get arguments passed ans env vars
    # env_vars = os.getenv("FLOWUI_K8S_EXECUTION_ENV_VARS")
    # env_dict = ast.literal_eval(env_vars)

    # Import Operator from File System, already configured with metadata
    volume_mount_path = os.getenv("VOLUME_MOUNT_PATH_DOCKER", "/opt/mnt/fs/airflow")
    operator_name = os.getenv("FLOWUI_BASHOPERATOR_OPERATOR_NAME")
    operators_folder_path = Path(volume_mount_path) / f"code_repository/operators"
    compiled_metadata_path = Path(volume_mount_path) / "code_repository/.flowui/compiled_metadata.json"
    with open(str(compiled_metadata_path), "r") as f:
        compiled_metadata = json.load(f)

    operator_class = load_operator_class_from_path(
        operators_folder_path=operators_folder_path,
        operator_name=operator_name,
        operator_metadata=compiled_metadata[operator_name]
    )

    operator_input_model_class, operator_output_model_class = load_operator_models_from_path(
        operators_folder_path=operators_folder_path,
        operator_name=operator_name
    )

    # Instantiate and run Operator
    instantiate_op_dict = ast.literal_eval(os.getenv("FLOWUI_BASHOPERATOR_INSTANTIATE_OP_KWARGS"))
    operator_object = operator_class(**instantiate_op_dict)

    run_op_dict = ast.literal_eval(os.getenv("FLOWUI_BASHOPERATOR_RUN_OP_KWARGS"))

    # Get relevant airflow context from ENV
    airflow_context = {
        "dag_owner": os.getenv('AIRFLOW_CONTEXT_DAG_OWNER'),
        "dag_id": os.getenv('AIRFLOW_CONTEXT_DAG_ID'),
        "task_id": os.getenv('AIRFLOW_CONTEXT_TASK_ID'),
        "execution_date": os.getenv('AIRFLOW_CONTEXT_EXECUTION_DATE'),
        "try_number": os.getenv('AIRFLOW_CONTEXT_TRY_NUMBER'),
        "dag_run_id": os.getenv('AIRFLOW_CONTEXT_DAG_RUN_ID'),
        "upstream_task_ids": os.getenv('AIRFLOW_CONTEXT_UPSTREAM_TASK_IDS')  # Added by FlowUI extended BashOperator
    }

    operator_object.run_operator_function(
        operator_input_model=operator_input_model_class, 
        operator_output_model=operator_output_model_class, 
        op_kwargs=run_op_dict,
        airflow_context=airflow_context
    )

    return None