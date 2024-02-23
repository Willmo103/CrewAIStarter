# Creating Custom Agents

This guide explains how to create custom AI agents using your CrewAI framework. Each agent encapsulates an Ollama language model and defines methods for specific functionalities.

## Structure

Each file in this directory should represent a single agent. The file name should be the name of the agent, and the file should contain a class with the same name. The class should inherit from `Agent` and implement the required methods.

```python
from crewai.agent import Agent

class MyAgent(Agent):
    def __init__(self):
        super().__init__()

    def on_message(self, message):
        pass

    def on_command(self, command):
        pass

    def on_event(self, event):
        pass
```

## Methods

### on_message

This method is called when the agent receives a message from the user. The message is passed as an argument to the method.

 ```python
 def on_message(self, message):
    pass
 ```

### on_command

This method is called when the agent receives a command from the user. The command is passed as an argument to the method.

 ```python
 def on_command(self, command):
    pass
 ```

### on_event

This method is called when the agent receives an event from the environment. The event is passed as an argument to the method.

 ```python
 def on_event(self, event):
    pass
 ```

## Example

Here is an example of a simple agent that responds to messages with a predefined response.

```python
from crewai.agent import Agent

class SimpleAgent(Agent):
    def __init__(self):
        super().__init__()

    def on_message(self, message):
        self.send_message("Hello, I am a simple agent!")

    def on_command(self, command):
        pass

    def on_event(self, event):
        pass
```
