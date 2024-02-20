# Defining Crew Tasks

This guide outlines creating well-structured tasks for your CrewAI framework. Tasks define input, output, and execution logic for specific jobs your crew performs.

## Structure

Place your task files within the tasks directory.
Each file defines a class inheriting from TaskBase (found in core.py).

**Specify essential properties:**

- description: A clear description of the task.
- input: The expected data format for the task.
- output: The expected data format for the task's result.
- Implement the execute method to define how the task works.

## Example

    ```python
    from tasks.core import TaskBase

    class CreateMarkdownCheatsheet(TaskBase):

    description = "Condense information into a Markdown cheatsheet."
    input = {"prompt": str, "backstory": str}
    output = str

    def execute(self, prompt, backstory):
        # Use agents, tools, and resources to create the cheatsheet
        # ...
        return cheatsheet_markdown
    ```

## Tips

- Design modular tasks with clear input/output specifications.
- Break down complex tasks into smaller, manageable units.
- Consider error handling and data validation for robust tasks.
