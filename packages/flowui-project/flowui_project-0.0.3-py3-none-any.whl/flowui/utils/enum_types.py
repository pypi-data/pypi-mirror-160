from enum import Enum


# Enum type for deploy_mode
class DeployModeType(Enum):
    local = 'local'
    kubernetes = 'kubernetes'
    aws_batch = 'aws_batch'
    aws_lambda = 'aws_lambda'
