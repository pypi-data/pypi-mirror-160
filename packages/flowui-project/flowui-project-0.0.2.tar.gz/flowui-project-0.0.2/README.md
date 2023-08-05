# FlowUI Project
An architecture for streamlining the production of Operators and the provisioning of Cloud infrastructure for Apache Airflow, with an interactive GUI for workflows creation!

Some points which we are trying to put together with FlowUI:
- make extensive use of Airflow for workflows management
- standardize the production of Operators that could run either on Batch Jobs, Kubernetes pods or locally (the same machine serving Airflow)
- these could serve heavy ML as well as light dataset updating workflows
- automatically import the list of Operators to a web GUI where the users could create their own workflows
- a more user friendly GUI for workflows supervision and management

Our goal is to build an architecture that abstracts the logics behind some of these points and automatizes as much as possible the continuous delivery lifecycle.

<p align="center">
<img src="docs/continuous_delivery.png" width="256"/>
</p>

<br>

# FlowUI Project - AWS Infrastructure

Per Platform:
- Frontend server
- Backend server
- Airflow server
- Database
- Code repository with collection of Operators (Github)
- Container resgistry with Docker images to run Operators
- Job definitions on AWS Batch: one per Operator (also per user? EFS mount limitation)
- Kubernetes infra ([helm charts](https://airflow.apache.org/docs/helm-chart/stable/index.html))

Per user of the platform:
- S3 bucket: for cheapest storage of all user’s data
- EFS: for shared storage between Tasks at DAG runtime

<br>

## Airflow instance
We still don't know if we should spin up one separate Airflow running instance per user, to be decided!

The Airflow instance should have access to a mounted EFS volume, shared with the other registered resources (Batch Job Definitions, Lambdas, ...). This volume is where the running Airflow will find its DAG files, the available Operator functions, plugins, and where it will store its logs.

For each running Airflow instance, these are the ENV variables that must be defined:
- `AWS_REGION_NAME`: aws region name, must be the same for all resources registered
- `AWS_BATCH_JOB_DEFINITION_{operator_name}_{operator_version}`: the job definition arn, one for each registered Operator
- `AWS_BATCH_JOB_QUEUE_{operator_name}_{operator_version}`: the job queue arn, one for each registered Operator
- ...

<br>

## File System structure:
In principle, user-specific data would be stored in S3. The loading of specific artifacts onto mounted File Systems (such as AWS EFS) could be done as per request of an Operator (LoadDatasetOperator, LoadModelOperator, etc…) so heavy data would be readily available to the containers running Jobs.
EFS pricing is not too bad, but it is twice the price of S3. It also charges per data transfer. So we would need to devise some housekeeping rules to clean / transfer the artifacts and runs results back to S3 (e.g. every 24 hours or something).
A mounted File System would also serve as the source of dags, logs and plugins for Airflow.
A mounted File System would also serve as the source of Operators files, synced with the code repository and readily accessible to the instances running the tasks.
A mounted File System would also serve as a temporary location for Tasks results that might be useful to downstream Tasks.

```
/

/airflow
..../logs
..../plugins
..../dags
......../workflow_1.py
......../workflow_2.py

/code_repository
..../dependencies
......../dependencies_map.json
..../operators
......../{operator-name}
............/metadata.json    # OPTIONAL
............/model.py         # REQUIRED
............/operator.py      # REQUIRED

/dataset
..../{dataset-id}
......../file1.mat
......../file2.csv
......../file3.json

/runs
..../{dag-id}
......../{run-id}
............/{task-id}
................/log.txt
................/result.npy
................/result.html
```

<br>

## Operators
We write the Operators ourselves, and this will be the main customizable point for each project. Each Operator will have:
- A `operator.py` file with the custom code to be executed, the `operator_function()`
- A `metadata.py` file containing the Operators metadata and frontend node style
- A `model.py` file containing the Pydantic model that defines the input of the `operator_function()`

Depending on how the Operators will be running:
- If running on AWS Batch, a Job Definition with:
    - A container image that runs this Operator
    - A Role with necessary permissions (access to EFS, S3, Database, etc…)
    - Mount of the EFS (how to make it if one EFS per user?)
    - Batch Compute Environment and Queue this Job is going to use
    - Other specific configurations (vcpu, ram, retries… can be changed at Job submit)
- If running locally (or on the same server as Airflow):
    - A container image that runs this Operator

<br>


## ENV vars
ENV vars definition levels:

**Host ENV**
- GITHUB_ACCESS_TOKEN
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION_NAME
- FLOWUI_PATH_HOST  (only for local dev)

**config.ini**
- PROJECT_NAME
- FLOWUI_DEPLOY_MODE
- VOLUME_MOUNT_PATH_HOST
- CODE_REPOSITORY_SOURCE
- GITHUB_REPOSITORY_NAME

**FlowUI CLI**
- CODE_REPOSITORY_PATH
- AIRFLOW_UID

**docker-compose.yaml**
- FLOWUI_PATH_DOCKER
- VOLUME_MOUNT_PATH_DOCKER
- AIRFLOW_HOME
- AIRFLOW__CORE__EXECUTOR
- AIRFLOW__CORE__SQL_ALCHEMY_CONN
- AIRFLOW__CELERY__RESULT_BACKEND
- AIRFLOW__CELERY__BROKER_URL
- AIRFLOW__CORE__FERNET_KEY
- AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION
- AIRFLOW__CORE__LOAD_EXAMPLES
- AIRFLOW__CORE__ENABLE_XCOM_PICKLING
- AIRFLOW__API__AUTH_BACKEND
- _PIP_ADDITIONAL_REQUIREMENTS
- AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL
