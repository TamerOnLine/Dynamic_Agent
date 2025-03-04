# main.py
from agent.agent import Agent


def main():
    """Run the AI agent and interact with the user."""
    agent = Agent()

    while True:
        try:
            user_query = input(
                "Ask about the weather or stock prices (or type 'exit' to quit): "
            ).strip()

            if user_query.lower() in ["exit", "quit"]:
                print("Program terminated. Goodbye!")
                break

            response = agent.process(user_query)
            print(f"Response: {response}")

        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
