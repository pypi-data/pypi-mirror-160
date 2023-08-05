from pathlib import Path
import importlib
import sys
import json


def load_operator_class_from_path(operators_folder_path: str, operator_name: str, operator_metadata: dict):
    # Import Operator from mounted volume, then set up operator module and class
    operators_folder_path = str(Path(operators_folder_path).resolve())
    if operators_folder_path not in sys.path:
        sys.path.append(operators_folder_path)

    importlib.invalidate_caches()
    operator_module = importlib.import_module(f"{operator_name}.operator")
    operator_class = getattr(operator_module, operator_name)

    # Set Operator class metadata
    operator_class.set_metadata(metadata=operator_metadata)

    return operator_class


def load_operator_models_from_path(operators_folder_path: str, operator_name: str):
    # Import Operator from mounted volume, then set up operator module and class
    operators_folder_path = str(Path(operators_folder_path).resolve())
    if operators_folder_path not in sys.path:
        sys.path.append(operators_folder_path)

    importlib.invalidate_caches()
    operator_model_module = importlib.import_module(f"{operator_name}.models")
    operator_input_model_class = getattr(operator_model_module, "InputModel")
    operator_output_model_class = getattr(operator_model_module, "OutputModel")

    return operator_input_model_class, operator_output_model_class