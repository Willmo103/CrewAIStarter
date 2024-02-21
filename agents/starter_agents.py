"""
# AgentsGroup

The agent Class from crewai.Agent can include the following init keyword arguments:

```python

agent = Agent(
    @kwarg: role: str -- The role of the agent.

    @kwarg: goal: str -- The end-goal of the agent. One sentence that describes the
    overarching goal of the agent.

    @kwarg: backstory: str -- The backstory serves as the motivation for the agent's
    goal. This can be thought of as a system prompt. It is a string that describes the
    agent's motivation, methods, and goal. This can be a multi-line string. You can
    use triple quotes like this:

        \"\"\"<backstory_text>\"\"\"

    for multi-line strings.

    @kwarg: tools: [Tool] -- Set of capabilities in the form of Tool class objects
    (defined in the /tools module) that grant the agent ability perform tasks
    outside of it's own knoweledge or ability by defining an interface for the model
    to seek knowledge, create content, or otherwise interact with the outside world
    in any way you define within the framework see [custom tool creation guide](https://google.com). TODO add link
    Tools can be shared or exclusive to specific agents.
    llm: language model -- This will be configured in the BaseCustomAgent class using the Ollama api and should only be configured in the BaseCustomAgent class.
    function_calling_llm=my_llm -- This will be configured in the BaseCustomAgent class using the Ollama api and should only be configured in the BaseCustomAgent class.
    max_iter=10 -- This will be configured in the BaseCustomAgent class using the Ollama api and should only be configured in the BaseCustomAgent class.
    max_rpm=10 -- This will be configured in the BaseCustomAgent class using the Ollama api and should only be configured in the BaseCustomAgent class.
    verbose=True, -- Using the CrewAI default option for verbose output.
    allow_delegation=True, -- Using the CrewAI default option for allowing delegation. This can be set to False if the agent is not allowed to delegate tasks.
    step_callback=my_intermediate_step_callback, -- This will be configured in the BaseCustomAgent class using the Ollama api and should only be configured in the BaseCustomAgent class, but can be overridden in the agent class or user defined agent class.
)
```
"""

from crewai import Agent
