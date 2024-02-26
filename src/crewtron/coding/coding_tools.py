import subprocess
import uuid
from langchain.agents import Tool
# from langchain__experimental.utilities import PythonREPL


from langchain.tools import tool
from pydantic import BaseModel


class DockerExecutionInput(BaseModel):
    command: str


class DockerFileInput(BaseModel):
    content: str


class AskQuestionInput(BaseModel):
    question: str


class CreateDockerContainerInput(BaseModel):
    dockerfile_content: str


class WriteCodeInput(BaseModel):
    file_path: str
    code_content: str


class SaveOutputInput(BaseModel):
    filename: str
    content: str


class STDOutput(BaseModel):
    output: str


class DockerCreationOutput(BaseModel):
    container_id: str


class BasicTools:
    @tool("Ask the customer for input", args_schema=AskQuestionInput, return_direct=True)
    def ask_question(self, args: AskQuestionInput) -> str:
        """Simulate asking a question to the user via terminal input."""
        print(args.question)
        return input("Answer: ")

    @tool("Get the current date", return_direct=True)
    def get_current_date(self) -> str:
        """Get the current date."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

    @tool("Write results to a file", args_schema=SaveOutputInput, return_direct=True)
    def save_output(self, args: SaveOutputInput) -> str:
        """Save content to a file."""
        with open(args.filename, 'w') as file:
            file.write(args.content)
        return f"Output saved to {args.filename}"


class DockerTools:
    def __init__(self, dockerfile_content=None):
        """Initialize a Docker environment from a Dockerfile, if provided."""
        self.container_id = None
        if dockerfile_content:
            self.image_name = f"custom_{uuid.uuid4()}"
            self.build_image(dockerfile_content, self.image_name)
            self.container_id = self.create_container(self.image_name)

    @tool("Build a Docker image from the provided Dockerfile content", args_schema=CreateDockerContainerInput, return_direct=True)
    @classmethod
    def build_image(cls, args: CreateDockerContainerInput) -> DockerCreationOutput:
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

    @tool("Run a command in the development environment", args_schema=DockerExecutionInput, return_direct=True)
    def run_docker_command(self, args: DockerExecutionInput) -> STDOutput:
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

    @tool("Write code to a file within the development environment", args_schema=WriteCodeInput, return_direct=True)
    def write_code(self, args: WriteCodeInput) -> str:
        """Write code to a file within the Docker container."""
        # Escape double quotes for shell command
        escaped_code = args.code_content.replace('"', '\\"')
        command = f'echo "{escaped_code}" > {args.file_path}'
        self.run_docker_command(DockerExecutionInput(command=command))
        print(f"Code written to {args.file_path} in container.")

    @tool("Run a specific command, such as a script, within the development environment")
    def run_code(self, args: DockerExecutionInput) -> STDOutput:
        """Run a specific command, such as a script, within the Docker container."""
        output = self.run_docker_command(args)
        print(f"Output from running command '{args.command}':\n{output}")
        return output

    @tool("Update the development environment with a new Dockerfile", args_schema=DockerFileInput, return_direct=True)
    def update_docker_env(self, args: DockerFileInput) -> DockerCreationOutput:
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

    @tool("Run a bash command", return_direct=True)
    def test_bash_command(self, command: str) -> str:
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
