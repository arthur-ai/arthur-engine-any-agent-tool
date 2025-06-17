import os
import uuid

from any_agent import AnyAgent, AgentConfig
from src.tools import ArthurTool

ARTHUR_ENGINE_URL=os.environ["ARTHUR_ENGINE_URL"]
ARTHUR_API_KEY=os.environ["ARTHUR_API_KEY"]
ARTHUR_TASK_ID=os.environ["ARTHUR_TASK_ID"]
CONVERSATION_ID=str(uuid.uuid4())
USER_ID=str(uuid.uuid4())


def main():
    # Initialize the Arthur tool with your credentials
    arthur_tool = ArthurTool(
        task_id=ARTHUR_TASK_ID,
        conversation_id=CONVERSATION_ID,
        user_id=USER_ID,
        host=ARTHUR_ENGINE_URL,
        api_key=ARTHUR_API_KEY,
    )

    # Create an AnyAgent instance with the Arthur tool
    agent = AnyAgent.create(
        "tinyagent",
        AgentConfig(
            model_id="gpt-4.1-nano",
            instructions="Generate a response to the user's query, then call the arthur_tool to validate the "
                         "user's prompt and your response before returning your response to the end user. "
                         "You can pass the prompt/response directly to the tool without adding additional instructions "
                         "or modifying it in any way.",
            tools=[arthur_tool],
        )
    )
        

    # Example usage
    prompt = "What is the capital of France?"
    
    # The agent will use the Arthur tool to validate the prompt and response
    response = agent.run(prompt)
    
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")

if __name__ == "__main__":
    main()
