class InvalidOperatorOutputError(Exception):
    """
    Raised when the Operator's output data is not an instance of the Operator's OutputModel
    """

    def __init__(self, operator_name: str):
        message = f"The output data for {operator_name} is not an instance of its OutputModel"
        super().__init__(message)