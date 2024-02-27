import subprocess, os
import uuid
from crewai.tools import tool
from crewtron.config import _docker, _CACHE as _cache

def build_image(args):
    """Build a Docker image from the provided Dockerfile content."""
    dockerfile_path = "/tmp/Dockerfile"
    image_name = f"custom_{uuid.uuid4()}"
    with open(dockerfile_path, "w") as file:
        file.write(args.dockerfile_content)
    result = subprocess.run(f"docker build -t {image_name} -f {dockerfile_path} .", shell=True, capture_output=True, text=True)
    if result.stderr:
        print("Error:", result.stderr)
        return None
    return result.stdout

def run_docker_command(container_id, command):
    """Run a command in the initialized Docker container."""
    if container_id is None:
        print("Error: No container is initialized.")
        return None
    cmd = f"docker exec {container_id} {command}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stderr:
        print("Error:", result.stderr)
        return None
    return result.stdout

def write_code(container_id, code_content, file_path):
    """Write code to a file within the Docker container."""
    # Escape double quotes for shell command
    escaped_code = code_content.replace('"', '\\"')
    command = f'echo "{escaped_code}" > {file_path}'
    run_docker_command(container_id, command)
    print(f"Code written to {file_path} in container.")

def run_code(container_id, command):
    """Run a specific command, such as a script, within the Docker container."""
    output = run_docker_command(container_id, command)
    print(f"Output from running command '{command}':\n{output}")
    return output

def update_docker_env(args):
    """Update the development environment with a new Dockerfile."""
    container_id = None
    return build_image(args)

class DockerTools:
    def __init__(self, dockerfile_content=None):
        """Initialize a Docker environment from a Dockerfile, if provided."""
        self.container_id = None
        if dockerfile_content:
            self.image_name = f"custom_{uuid.uuid4()}"
            self.build_image(dockerfile_content, self.image_name)
            self.container_id = self.create_container(self.image_name)

    @tool("Build a Docker image from the provided Dockerfile content", return_direct=True)
    @classmethod
    def build_image(cls, args) -> DockerCreationOutput:
        return build_image(args)

    @tool("Run a command in the development environment", return_direct=True)
    def run_docker_command(self, args) -> STDOutput:
        return run_docker_command(self, args)

    @tool("Write code to a file within the development environment", return_direct=True)
    def write_code(self, args) -> str:
        write_code(self, args)

    @tool("Run a specific command, such as a script, within the development environment")
    def run_code(self, args) -> STDOutput:
        return run_code(self, args)

    @tool("Update the development environment with a new Dockerfile", return_direct=True)
    def update_docker_env(self, args) -> DockerCreationOutput:
        return update_docker_env(self, args)


class BasicTools:
    @tool("Ask the customer for input", return_direct=True)
    def ask_question(self, question: str) -> str:
        """Simulate asking a question to the user via terminal input."""
        print(question)
        return input("Answer: ")

    @tool("Get the current date", return_direct=True)
    def get_current_date(self) -> str:
        """Get the current date."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

    @tool("Write results to a file", return_direct=True)
    def save_output(self, filename: str, content: str) -> str:
        """Save content to a file."""
        with open(os.path.join(_cashe, filename, 'w') as file:
            file.write(content)
        return f"Output saved to {args.filename}"


class DockerTools:
    def __init__(self, dockerfile_content=None):
        """Initialize a Docker environment from a Dockerfile, if provided."""
        self.container_id = None
        if dockerfile_content:
            self.image_name = f"custom_{uuid.uuid4()}"
            self.build_image(dockerfile_content, self.image_name)
            self.container_id = self.create_container(self.image_name)

    @tool("Build a Docker image from the provided Dockerfile content", return_direct=True)
    @classmethod
    def build_image(cls, args) -> DockerCreationOutput:
        """Build a Docker image from the provided Dockerfile content."""
        dockerfile_path = "/tmp/Dockerfile"
        image_name = f"custom_{uuid.uuid4()}"
        with open(dockerfile_path, "w") as file:
            file.write(args.dockerfile_content)
        result = subprocess.run(f"docker build -t {image_name} -f {dockerfile_path} .", shell=True, capture_output=True, text=True)
        if result.stderr:
            print("Error:", result.stderr)
            return None
        return DockerCreationOutput(container_id=result.stdout.strip())

    @tool("Run a command in the development environment", return_direct=True)
    def run_docker_command(self, args) -> STDOutput:
        """Run a command in the initialized Docker container."""
        if self.container_id is None:
            print("Error: No container is initialized.")
            return None
        cmd = f"docker exec {self.container_id} {args.command}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stderr:
            print("Error:", result.stderr)
            return None
        return STDOutput(output=result.stdout)

    @tool("Write code to a file within the development environment", return_direct=True)
    def write_code(self, args) -> str:
        """Write code to a file within the Docker container."""
        # Escape double quotes for shell command
        escaped_code = args.code_content.replace('"', '\\"')
        command = f'echo "{escaped_code}" > {args.file_path}'
        self.run_docker_command(DockerExecutionInput(command=command))
        print(f"Code written to {args.file_path} in container.")

    @tool("Run a specific command, such as a script, within the development environment")
    def run_code(self, args) -> STDOutput:
        """Run a specific command, such as a script, within the Docker container."""
        output = self.run_docker_command(args)
        print(f"Output from running command '{args.command}':\n{output}")
        return output

    @tool("Update the development environment with a new Dockerfile", return_direct=True)
    def update_docker_env(self, args) -> DockerCreationOutput:
        """Update the development environment with a new Dockerfile."""
        self.container_id = None
        return self.build_image(args)


class BashEnvironment:
    def __init__(self):
        self.container_name = uuid.uuid4()
        self.create_container(self.container_name)

    def create_container(self, container_name):
        result = subprocess.run(f"docker run -d --name {container_name} -it ubuntu", shell=True, capture_output=True, text=True)
        if result.stderr:
            print("Error:", result.stderr)
            return None
        return result.stdout.strip()

    @tool("Run a bash command in a dev environment", return_direct=True)
    def test_bash_command(command: str) -> str:
        """Run a bash command."""
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout


class PythonEnvironment:
    def __init__(self):
        self.container_name = uuid.uuid4()
        self.create_container(self.container_name)

    def create_container(self, container_name):
        result = subprocess.run(f"docker run -d --name {container_name} -it python:3.8", shell=True, capture_output=True, text=True)
        if result.stderr:
            print("Error:", result.stderr)
            return None
        return result.stdout.strip()

    @tool("Run a Python command", return_direct=True)
    def test_python_command(self, command: str) -> str:
        """Run a Python command."""
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout


@tool("Create an environment for Python code execution", return_direct=True)
def create_python_environment() -> PythonEnvironment:
    """Create an environment for Python code execution."""
    return PythonEnvironment()


@tool("Create an environment for Bash command execution", return_direct=True)
def create_bash_environment() -> BashEnvironment:
    """Create an environment for Bash command execution."""
    return BashEnvironment()


@tool("Create a Docker environment from a Dockerfile", args_schema=DockerFileInput, return_direct=True)
def create_docker_environment(args: DockerFileInput) -> DockerTools:
    """Create a Docker environment from a Dockerfile."""
    return DockerTools(dockerfile_content=args.content)
