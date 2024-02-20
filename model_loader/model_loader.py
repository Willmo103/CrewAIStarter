from model_loader.custom_model import CustomModel

class ModelLoader:

    models = {
        'summarizer': CustomModel({
            'model_name': 'summarizer',
            'modelfile': """""",
            'temperature': 0.7,
        }),
    }

    @classmethod
    def pull_or_create(cls, model_name: str, **kwargs) -> CustomModel:
        if model_name not in cls.models:
            model = CustomModel(model_name, **kwargs)
            if not model.pull():
                model.create()
            cls.models[model_name] = model
        return cls.models[model_name]
