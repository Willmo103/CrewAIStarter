import subprocess
import os
from crewtron import config


class BaseEnvironment:
    id: str
    dockerfile: str
    docker_compose: str
    volume: str
    workspace: str
    container: str
    entrypoint: str
    files: list[str]

    def execute(self, command: str) -> str:
        result = subprocess.run(
            f"docker exec {self.id} {command}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.stdout.decode("utf-8")

    def create(self):
        self.id = config._PROCESS_UUID
        self.workspace = os.path.join(config.DOCKER, self.id)
        self.volume = os.path.join(self.workspace, self.id + '_volume')

        file_data = [
            ('Dockerfile', self.dockerfile),
            ('docker-compose.yml', self.docker_compose),
            ('entrypoint.sh', self.entrypoint),
            ('.dockerignore', 'Dockerfile\ndocker-compose.yml')
        ]

        os.makedirs(self.volume, exist_ok=True)

        for file_name, content in file_data:
            with open(os.path.join(self.workspace, file_name), 'w') as f:
                f.write(content)
            f.write('Dockerfile\ndocker-compose.yml')

        os.makedirs(self.volume, exist_ok=True)

        build_result = subprocess.run(
            f"docker build -t {self.id} {self.workspace}",
            shell=True,
            capture_output=True
        )
        if build_result.returncode != 0:
            raise Exception(build_result.stderr.decode("utf-8"))

        run_result = subprocess.run(
            f"docker docker-compose -f {self.workspace}/docker-compose.yml up -d",
            shell=True,
            capture_output=True
        )

        if run_result.returncode != 0:
            raise Exception(run_result.stderr.decode("utf-8"))

        self.id = run_result.stdout.decode("utf-8").strip()

    def update(self, dockerfile: str = "", docker_compose: str = "", entrypoint: str = "", files: list[str] = []):
        self.dockerfile = dockerfile
        self.docker_compose = docker_compose
        self.entrypoint = entrypoint
        self.create()
