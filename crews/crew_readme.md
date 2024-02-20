# Building Effective Crews

This guide explains how to assemble powerful crews from your agents, tools, and tasks. Crews orchestrate interactions between components to achieve your desired outcomes.

## Structure

- Place your crew files within the `crews` directory.
- Each file defines a class inheriting from CrewBase (found in core.py).
- **Specify crew composition:**
  - agents: A list of agent instances from the agents directory.
  - tasks: A list of task instances from the tasks directory.
  - tools: A list of tool instances from the tools directory (if applicable).
- Define crew behavior:
  - Implement methods to orchestrate interactions between agents, tools, and tasks.
  - Utilize data flow management and error handling mechanisms.

## Example

  ```python

  from crews.core import CrewBase

  class ContentCreationCrew(CrewBase):

      def create_markdown_cheatsheet(self, prompt, backstory):
          researcher = self.agents["researcher"]
          writer = self.agents["writer"]
          duckduckgo = self.tools["duckduckgo"]

          # Use researcher and duckduckgo to gather relevant information
          research_summary = researcher.summarize(duckduckgo.search(prompt))

          # Use writer to create the cheatsheet based on the summary
          cheatsheet = writer.generate_text(f"Cheatsheet on: {prompt}", backstory=backstory, summary=research_summary)

          return cheatsheet
  ```

## Tips

- **Keep crews focused:** Each crew should handle a specific set of tasks.
  - Design crews with clear goals and well-defined workflows.
- Test your crew thoroughly with various inputs and scenarios.
  - Ensure that agents, tools, and tasks interact as expected.
  - Implement error handling and logging to capture and address issues.
  - Use data flow management to track and manage information flow between components.
- **Leverage existing components:** Reuse agents, tools, and tasks across multiple crews.
  - This reduces redundancy and ensures consistency across your projects.
