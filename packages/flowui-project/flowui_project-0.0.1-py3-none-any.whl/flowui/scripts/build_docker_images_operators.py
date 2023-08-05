from pathlib import Path
import docker
import json
import os

def build_images_from_code_repository(code_repository: str = None):
    client = docker.from_env()

    if code_repository is None:
        code_repository = Path(".")

    dependencies_path = Path(code_repository) / "dependencies"
    flowui_path = Path(code_repository) / ".flowui"

    cwd = Path.cwd()
    code_repository_absolute = Path(code_repository).resolve()
    code_repository_ctx_relative = Path(os.path.relpath(code_repository_absolute, cwd))

    # Load dependencies_map.json file
    with open(flowui_path / "dependencies_map.json", "r") as f:
        operators_images_map = json.load(f)

    # Build docker images from unique definitions
    for k, v in operators_images_map.items():

        # If dependency is defined as a docker image
        if v["dependency"].get("docker_image", None):
            # TODO
            continue

        # If dependency is defined as a Dockerfile
        elif v["dependency"].get("dockerfile", None):
            dockerfile = v["dependency"].get("dockerfile")
            try:
                print(f"Building docker image: {k}")
                img = client.images.build(
                    path=str(dependencies_path.resolve()),
                    dockerfile=dockerfile,
                    tag=k,
                    rm=True
                )
                print(f"Finished building: {k}")
            except Exception as e:
                raise Exception(e)
            continue

        # If dependency is defined as a requirements.txt
        elif v["dependency"].get("requirements_file", None):
            requirements_file = v["dependency"].get("requirements_file")
            requirements_str = f"""
USER airflow
COPY {Path('dependencies') / requirements_file} .
RUN pip install --user virtualenv \
    && virtualenv flowui_env --system-site-packages\
    && source flowui_env/bin/activate \
    && /opt/airflow/flowui_env/bin/pip install --upgrade pip \
    && pip install --no-cache-dir -r {requirements_file}
"""

        else:
            requirements_str = ""

        dockerfile_str = f'''FROM "apache/airflow:2.3.3-python3.8"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

{requirements_str}
'''     
        dockerfile_path = code_repository_ctx_relative / "Dockerfile"
        with open(str(dockerfile_path), "w") as f:
            f.write(dockerfile_str)
        
        try:
            print(f"Building docker image: {k}")
            img = client.images.build(
                path=str(dockerfile_path.parent),
                dockerfile="Dockerfile",
                tag=k,
                rm=True
            )
            print(f"Finished building: {k}")
        except Exception as e:
            raise Exception(e)
        finally:
            dockerfile_path.unlink()    
        continue
    
    return None