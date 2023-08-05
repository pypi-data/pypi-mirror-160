from pydantic import BaseModel, Field
from typing import List, Dict


class Dependency(BaseModel):
    docker_base_image: str = Field(
        description="Docker image to be used as base for the container that will run this Operator", 
        example="python:3.9-slim", 
        default=None
    )
    dockerfile: str = Field(
        description="Dockerfile to build the image for the container that will run this Operator", 
        example="Dockerfile", 
        default=None
    )
    requirements_file: str = Field(
        description="Requirements file with pip packages to be installed in the container that will run this Operator", 
        example="requirements.txt",
        default=None
    )


class InputSchema(BaseModel):
    title: str
    description: str
    type: str
    properties: Dict


class OperatorMetadata(BaseModel):
    name: str = Field(
        description="Operator name", 
        example="ExampleOperator", 
        # regex=    # TODO - regex for *Operator  
    )
    version: str = Field(
        description="Operator version", 
        example="0.1.0", 
        # regex=    # TODO - regex for 0.1.0 type
    )
    dependency: Dependency = None
    tags: List[str] = None
    style: Dict = None # TODO - add model for the style dictionary
    input_schema: InputSchema = None