# CrewAI Starter Guide

Welcome to the exciting world of CrewAI! This guide will help you build your own custom crew package, complete with Agents, Tasks, Crews, Tools, and ModelLoaders. Don't worry if you're a Jr. dev or a newcomer – we'll break it down step-by-step with clear explanations and helpful tips.

----

## Project Setup

**Create a Directory:**
Let's start by making a new folder for your crew package. Open your terminal and type:

```Bash
mkdir crew_package
cd crew_package
```

**Install Dependencies**
We need some tools to build our crew. In your terminal, run:

```Bash
pip install -r requirements.txt
```

----

## Building Your Crew

Now, let's meet the stars of your crew:

----

## Agents

**What they are:**
These are the AI brains of your crew, responsible for processing information and generating responses.

**Creating an Agent:**
In the agents folder, create a new file (e.g., my_agent.py).
Inside, define a class with methods like respond to handle prompts and generate text.
Use langchain_community.llms.ollama.Ollama as your language model.
Check out the `/agents/starter_agent.py` example for inspiration.

----

## Tasks

**What they are:**
These are the specific jobs your crew needs to tackle.

**Creating a Task:**
In the tasks folder, create a new file (e.g., summarize_article.py).
Define a class with properties like description and input/output specifications.
Implement the execute method to define how the task works.
See the `/tasks/starter_tasks.py` example for a reference.

----

## Crews

**What they are:**
These are groups of agents and tools working together on tasks.

**Creating a Crew:**
In the crews folder, create a new file (e.g., content_creation_crew.py).
Define a class with properties like agents, tools, and tasks.
Specify which agents and tools are part of the crew and which tasks they handle.
Take a look at the `/crews/starter_crew.py` example for guidance.

----

## Tools

**What they are:**
These are helper functions or modules that your agents and tasks can use.

**Creating a Tool:**
In the tools folder, create a new file (e.g., text_cleaner.py).
Define functions that perform specific tasks, like cleaning text or generating reports.
See the `/tools/starter_tools.py` example for an idea.

----

## ModelLoaders

**What they are:**
The concept of a 'ModelLoader' is not a part of the CrewAI framework,
but a small integration to bring the power of Ollama to your crew. It allows you
to create Ollama Modelfiles to allow further customization and control over your
local language model. The base ModelLoader class manages the connection
The the Ollama API and provides a simple interface to download (or 'pulling')
models from OllamaHub and saving them to your local machine.

**Creating a ModelLoader:**
In the model_loaders folder, create a file like llama_loader.py.
Define a function download_and_create_model using os.environ['OLLAMA_BASE_URL'] and the model creation API.
Handle potential issues like authentication and caching.
Refer to the `/model_loaders/starter_loader.py` example for structure.

----

## Main Script

**What it does:**
This script brings everything together and runs your crew.
Creating the Script:
In main.py, import and create instances of your agents, tasks, crews, and tools.
Orchestrate interactions between them based on your application logic.
Use the model_loaders to create Ollama models if needed.
See `main.py` for a basic example.

----

### Tips

Start small! Begin with one agent, one task, and one crew.
Use meaningful names and comments to make your code clear.
Test each component thoroughly to ensure it works as expected.
Don't hesitate to consult documentation and examples online.
Most importantly, have fun and experiment!

----

### Additional Resources

CrewAI Documentation: [Here](https://docs.crewai.com/)
CrewAI GitHub Repository: [Here](https://docs.crewai.com/)
Chat With CrewAI Docs: [Here](https://chat.openai.com/g/g-qqTuUWsBY-crewai-assistant)
Ollama Modelfile Documentation: [Here](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
