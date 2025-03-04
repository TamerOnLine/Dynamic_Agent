import sys
import os
import importlib
import pkgutil
import logging
from agent.agent import Agent

# Add `src/` to `sys.path` to ensure `tools` can be imported
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_tools():
    """Load all tools from the `tools` directory using `os.listdir()`."""
    try:
        import tools
    except ModuleNotFoundError:
        logging.error("Cannot import `tools/`. Ensure `src/` is added to `sys.path`.")
        return []

    loaded_tools = []
    tools_dir = os.path.dirname(tools.__file__)  # Actual path of `tools/`

    logging.info(f"Searching for tools in: {tools_dir}")

    for file in os.listdir(tools_dir):
        if file.endswith("_tool.py") and file != "__init__.py":
            module_name = file[:-3]  # Remove `.py` extension
            try:
                logging.info(f"Attempting to load tool: {module_name}")
                module = importlib.import_module(f"tools.{module_name}")
                tool = getattr(module, module_name, None)

                if tool:
                    loaded_tools.append(tool)
                    logging.info(f"Tool loaded: {tool.name}")
            except Exception as e:
                logging.error(f"Error loading tool {module_name}: {e}")

    if not loaded_tools:
        logging.error("No tools were loaded. Ensure tools are correctly defined in `tools/`.")

    return loaded_tools

def main():
    """Run the agent with dynamically loaded tools."""
    tools = load_tools()
    
    if not tools:
        logging.error("No tools were loaded. Check `tools/` and ensure tools are correctly defined.")
        return

    agent = Agent(tools=tools)  # Pass loaded tools to `Agent`

    while True:
        try:
            user_query = input("\nEnter your question (or type 'exit' to quit): ").strip()
            
            if user_query.lower() in ["exit", "quit"]:
                logging.info("Program terminated. Goodbye!")
                break

            response = agent.process(user_query)
            print(f"Response: {response}")

        except KeyboardInterrupt:
            logging.warning("Program interrupted by user.")
            break
        except Exception as e:
            logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
