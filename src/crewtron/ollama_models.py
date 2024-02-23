from langchain_community.llms.ollama import Ollama
from crewtron.config import get_base_url

_base_url = get_base_url()

function_caller = Ollama(
    name="function_caller",
    base_url=_base_url,
    system="""
    You are a function caller. You are responsible for calling functions in the
    system. You are not responsible for the implementation of the functions, but
    you are responsible for ensuring that the functions are called correctly and
    that the results are handled properly. You are also responsible for ensuring
    """
)
