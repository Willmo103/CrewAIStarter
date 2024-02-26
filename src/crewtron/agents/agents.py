from crewai import Agent
from langchain_community.llms.ollama import Ollama

from crewtron.config import get_base_url, init_logger, log_time
from crewtron.modelfiles import modelfiles

# module-level logger
_log = init_logger().getChild(__name__)
_base_url = get_base_url()


@log_time
def build_ollama_agent(modelfile: str):
    try:
        _modelfile = load_model_file(modelfile)
        return Ollama(_modelfile)
    except Exception as e:
        _log.error(f"Error building Ollama agent: {e}")
        raise e


@log_time
def load_model_file(modelfile: str):
    try:
        mf = modelfiles[modelfile]
        return Ollama(mf)
    except Exception as e:
        _log.error(f"Error loading model file: {e}")
        raise e


class AgentGroup:
    agents = {
        "researcher": Agent(
            role="Research Analyst",
            goal="To provide insights and analysis on the latest trends in the market.",
            backstory="""
            You are a Research Analyst at a leading market research firm. Your job
            is to provide insights and analysis on the latest trends in the market.
            Over your career, you have developed a deep understanding of the market
            and have a knack for identifying trends before they become mainstream.
            You are known for your ability to provide actionable insights that help
            businesses make informed decisions. You are constantly on the lookout
            for new data sources and methodologies to improve your analysis.
            You are also skilled at distilling complex information into
            easy-to-understand reports and presentations.
            """,
            llm=_base_url,
        ),
    }
