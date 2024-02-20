# Leveraging Powerful Tools

This guide introduces tools in your CrewAI framework. Tools are helper functions or modules that expand your agents' and tasks' capabilities. You can leverage pre-built tools or create your own for specific needs.

## Structure

- Place tool files within the tools directory.
- Each file defines a function or class.
- Functions should be clearly named and documented, specifying parameters and return values.
- Classes should inherit from ToolBase (found in core.py) for consistent structure.

## Pre-built Example

    tools/duckduckgo_search.py: Implements a tool to search using DuckDuckGo.

## Custom Example

    ```python
    def convert_markdown_to_html(markdown):
        # Implement markdown to HTML conversion logic
        return html

    class DataPreprocessor:

        def clean_text(self, text):
            # Implement text cleaning logic
            return clean_text

    # Add more tools and functions as needed

    ```

## Tips

- Design modular tools with well-defined functionalities.
- Consider reusability and potential integration with other tools.
- Test your tools thoroughly with various inputs and scenarios.
