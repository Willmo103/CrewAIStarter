import subprocess
import os
from typing import Optional
from pydantic import BaseModel
from crewtron import config
from crewtron.config import log_v as env_log
from crewai_tools import tool

_docker = config.DOCKER
_uuid = config._PROCESS_UUID


class BaseEnvironment:
    id = _uuid
    workspace = os.path.join(_docker, id)
    volume = os.path.join(workspace, id + "_volume")
    dockerfile: str
    docker_compose: str
    container: str
    entrypoint: str
    files: list[str]

    class UpdateArgs(BaseModel):
        dockerfile: str
        docker_compose: Optional[str]
        entrypoint_sh: Optional[str]
        files: Optional[list[str]]

    @env_log("init_environment")
    def __init__(self):
        try:
            self.init_workspace()
            self.build_container()
            self.run_container()
        except Exception as e:
            raise Exception(e)

    @env_log("executing command in environment")
    @tool("execute commands in the environment")
    def execute(self, command: str) -> str:
        result = subprocess.run(
            f"docker exec {self.id} {command}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.decode("utf-8")

    @env_log("recreate environment")
    @tool(
        "Update the development environment with a new Dockerfile",
        args_schema=UpdateArgs,
    )
    def update(
        self, args: UpdateArgs
    ):
        """This tool can be used to further customize the environment by supplying
        contents of a new Dockerfile, docker-compose.yml, entrypoint.sh, and any other
        files that need to be added to the environment.

}
        """
        self.dockerfile = args.dockerfile
        self.docker_compose = args.docker_compose
        self.entrypoint = args.entrypoint_sh
        self.files = args.files
        self.init_workspace()
        self.build_container()
        self.run_container()

    @env_log("redeploy environment")
    def init_workspace(self):
        file_data = [
            ("Dockerfile", self.dockerfile),
            ("docker-compose.yml", self.docker_compose),
            ("entrypoint.sh", self.entrypoint),
            (".dockerignore", "Dockerfile\ndocker-compose.yml"),
        ]

        os.makedirs(self.volume, exist_ok=True)

        for file_name, content in file_data:
            if content:
                with open(os.path.join(self.workspace, file_name), "w") as f:
                    f.write(content)

        os.makedirs(self.volume, exist_ok=True)

    def build_container(self):
        output = subprocess.run(
            f"docker build -t {self.id} {self.workspace}",
            shell=True,
            capture_output=True,
        )

        if output.returncode != 0:
            raise Exception(output.stderr.decode("utf-8"))
        else:
            return True

    def run_container(self):
        if self.

        # output = subprocess.run(
        #     f"docker-compose -f {self.workspace}/docker-compose.yml up -d",
        #     shell=True,
        #     capture_output=True,
        # )

        # if output.returncode != 0:
        #     raise Exception(output.stderr.decode("utf-8"))
        # else:
        #     return True
