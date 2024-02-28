import os
import subprocess
from crewai.tools import tool
import psycopg2
from crewtron.config import config as _config
from crewai_tools import BaseTool
import crewai_tools as ct

logOutput = _config.log_v


@tool("User Input")
def user_input(question: str) -> str:
    """Ask the user for input in the form of a question for follow-up.
    Task specific information, or any other clarifying details.

    input: str - question

    output: str - answer
    """
    return input(f"Question: {question}\nAnswer: ")


@tool("Submit for Approval")
def submit_for_approval(results: str) -> str:
    """Submit your final results for approval by the customer. This
    Should always be the last step in the workflow. This will notify
    the customer that the task is complete and they can review the
    result, and suggest any changes if necessary.

    input: str - results

    output: str - approval status, approved or suggestions for changes.
    """
    return user_input(f"Results: {results}\nSubmit for Approval?")


@tool("run sql in postgres database")
def run_query(query: str) -> str:
    """Run a query on a postgres database.

    input: str - query

    output: str - results
    """
    try:
        conn = psycopg2.connect(_config.get_connection_string("crewai_test_db"))
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        return str(e)


class CodeEnvironment(BaseTool):
    name = "Ubuntu Development Environment"
    description = """
    Preform actions within a ubuntu development environment.The input of
    this tool can be a command to run, code to write or run, install any
    package or configuration to install. The input should be a string or
    aray of strings to be executed in the ubuntu environment.

    example:
    [ "apt-get update", "apt-get install -y python3"]
    'echo "print('Hello World')" > hello.py'
    git clone https://.../repo.git

    Try not to execute any command that will stop the container.

    Working dir: /src
    """

    def get_docker_compose(self, volume: str, dockerfile: str = "") -> str:
        if not dockerfile:
            return f"""
            Version: '3'

            Services:
                {self.container}:
                    image: ubuntu
                    volumes:
                        - {volume}:/src
                    working_dir: /src

               postgres:
                    image: postgres
                    environment:
                        POSTGRES_USER: postgres
                        POSTGRES_PASSWORD: postgres
                        POSTGRES_DB: postgres

            Volumes:
                {self.container}:
                pgdata:

            """
        else:
            return f"""
            Version: '3'

            Services:
                {self.container}:
                    build: {_config.TMP + '/' + self.container}
                    volumes:
                        - {volume}:/src
                    working_dir: /src

               postgres:
                    image: postgres
                    environment:
                        POSTGRES_USER: postgres
                        POSTGRES_PASSWORD: postgres
                        POSTGRES_DB: postgres

            Volumes:
                {self.container}:
                pgdata:
            """

    def init_container(self):
        global _config
        self.container = _config._PROCESS_UUID
        self.container_id = None
        self.volume = os.path.join(_config.DOCKER, self.container + '_' + self.container_id)
        os.makedirs(self.volume, exist_ok=True)
        try:
            _ = subprocess.run(f"docker run -itd --name {self.container} --restart unless-stopped --volume /{self.volume}:/src --workdir /src ubuntu", shell=True, capture_output=True)
            if _.stderr:
                logOutput(f"Error: {_.stderr}")
                return None
            self.container_id = _.stdout.strip()
        except Exception as e:
            logOutput(f"Error: {e}")
            return None

    def container_context(self, command: str) -> str:
        """Run a command in the development environment"""
        if not self.container_id:
            self.init_container()
        try:
            _ = subprocess.run(f"docker exec -it {self.container_id} {command}", shell=True, capture_output=True)
            if _.stderr:
                logOutput(f"Error: {_.stderr}")
                return None
            return _.stdout
        except Exception as e:
            logOutput(f"Error: {e}")
            return None

    def _run(self, command: str | list[str]) -> str:
        return self.container_context(command)
