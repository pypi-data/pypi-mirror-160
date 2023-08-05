from flowui.scripts.load_operator import load_operator_class_from_path, load_operator_models_from_path
from pathlib import Path
import os
import ast
import json


def run_operator():
    # Get arguments passed ans env vars
    env_vars = os.getenv("FLOWUI_K8S_EXECUTION_ENV_VARS")
    env_dict = ast.literal_eval(env_vars)

    # Import Operator from File System, already configured with metadata
    volume_mount_path = env_dict.get("VOLUME_MOUNT_PATH_DOCKER", "/opt/mnt/fs/airflow")
    operator_name = env_dict.get("FLOWUI_K8S_OPERATOR_NAME")
    operators_folder_path = Path(volume_mount_path) / f"code_repository/operators"
    compiled_metadata_path = volume_mount_path / "code_repository/.flowui/compiled_metadata.json"
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
    operator_object = operator_class(**env_dict.get("FLOWUI_K8S_INIT_OPERATOR_VARS"))

    operator_object.run_operator_function(
        operator_input_model=operator_input_model_class, 
        operator_output_model=operator_output_model_class, 
        **env_dict.get("FLOWUI_K8S_RUN_OPERATOR_VARS")
    )

    return None