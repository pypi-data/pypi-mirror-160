from .base_operator import BaseOperator


def create_operator(
    metadata: dict, 
    operator_function: callable, 
    generate_report: callable = None
):
    class NewOperator(BaseOperator): pass

    # Operator name as used by Airflow
    NewOperator.__name__ = metadata.get("name", "BaseOperator")

    # Operator version: update it to auto update the deployed version
    NewOperator.__version__ = metadata.get("version", "0.1.0")

    # Dockerfile to build Image for this function
    NewOperator.__dockerfile__ = metadata.get("dockerfile", "Dockerfile")
    
    # Operator custom function
    NewOperator.operator_function = operator_function

    # Operator custom Generate Report function
    if generate_report:
        NewOperator.generate_report = generate_report
    
    return NewOperator