from model_loader.custom_model import CustomModel
from langchain_community.llms.ollama import Ollama as LC_Ollama
from ollama import Client
from config import OLLAMA_API_URL
from textwrap import dedent
import os

MODELFILES_DIR = os.path.join(os.path.dirname(__file__), "model_files")
if not os.path.exists(MODELFILES_DIR):
    os.makedirs(MODELFILES_DIR)


class ModelFileException(Exception):
    pass


class ModelFile:
    name: str
    sys_msg: str
    model: str
    description: str

    def __init__(self, **kwargs) -> None:
        try:
            assert "name" in kwargs
            assert "sys_msg" in kwargs
            assert "model" in kwargs
        except AssertionError as e:
            raise ModelFileException(
                "ModelFile must have a name, sys_msg, and model"
            )
        self.name = kwargs["name"]
        self.sys_msg = kwargs["sys_msg"]
        self.model = kwargs["model"]
        if "description" in kwargs:
            self.description = kwargs["description"]
        else:
            self.description = ""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        return f"ModelFile(name={self.name}, sys_msg={self.sys_msg}, model={self.model})"

    def __repr__(self) -> str:
        return f"ModelFile(name={self.name}, sys_msg={self.sys_msg}, model={self.model})"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, ModelFile):
            return (
                self.name == o.name
                and self.sys_msg == o.sys_msg
                and self.model == o.model
            )
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return hash((self.name, self.sys_msg, self.model))

    def load(self):
        return dedent(
            f"""
        {self.render_description()}
        FROM {self.model}
        {self.render_params()}
        SYSTEM \"\"\"{self.sys_msg}\"\"\"
        """
        )

    def render_params(self):
        params = ""
        for key, value in self.__dict__.items():
            if key not in ["name", "sys_msg", "model", "description"]:
                params += f"PARAMETER {value}\n"
        return params if params else "\r"

    def render_description(self):
        desc = self.description.strip().replace("\n", " ")
        return f"# {self.name}\n# {desc}\n\n" if desc else f"# {self.name}\n\n"

    def save(self, path: str):
        with open(path + self.name + ".llm", "w") as f:
            f.write(self.load())
            f.close()


class BaseClient:
    def __init__(self):
        self._base_url = OLLAMA_API_URL
        self._ollama_api_client = Client(base_url=self.base_url)
        self._ollama = LC_Ollama(base_url=self.base_url)
        self._available_models = self._ollama_api_client.list()
        self.embedding_model = self._ollama_api_client

    def _create_model(self, model_file: ModelFile):
        self._ollama_api_client.create(model=model_file.name)

    def _check_model(self, name: str):
        return name in self._available_models

class ModelLoader(BaseClient):
    def __init__(self):
        super().__init__()

    def pull_or_create(self, model_file: ModelFile):
        if not self._check_model(model_file.name):
            self._create_model(model_file)
        return self._ollama.get(model_file.name)

    def pull(self, model_file: ModelFile):
        return self._ollama.


# class ModelLoader:

#     models = {
#         "summarizer": CustomModel(
#             {
#                 "model_name": "summarizer",
#                 "modelfile": """""",
#                 "temperature": 0.7,
#             }
#         ),
#     }

#     @classmethod
#     def pull_or_create(cls, model_name: str, **kwargs) -> CustomModel:
#         if model_name not in cls.models:
#             model = CustomModel(model_name, **kwargs)
#             if not model.pull():
#                 model.create()
#             cls.models[model_name] = model
#         return cls.models[model_name]
