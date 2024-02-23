from config import get_base_url

_base_url = get_base_url()

modelfiles = {
    "mistral_serious": {
        "base_url": _base_url,
        "name": "Mistral Serious",
        "description": "A serious model for serious business.",
        "system": """
        You are a serious model. You are responsible for handling serious business.
        You are to give serious consideration to the tasks and responsibilities that
        are assigned to you. You are to ensure that the tasks are handled with the
        utmost seriousness and that the results are handled with the utmost care.
        """,
        "temperature": 0.2,
        "max_tokens": 512,
    },
    "SQL_writer": {
        "base_url": _base_url,
        "name": "SQL Writer",
        "description": "A model for writing SQL queries.",
    }
}
