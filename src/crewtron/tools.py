from crewai.tools import tool
import psycopg2
from crewtron.config import config as _config
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
