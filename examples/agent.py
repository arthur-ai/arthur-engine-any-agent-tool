import os
from any_agent import AnyAgent, AgentConfig
from src.tools import ArthurTool

def main():
    # Initialize the Arthur tool with your credentials
    arthur_tool = ArthurTool(
        task_id="your-task-id",
        conversation_id="your-conversation-id",
        user_id="your-user-id",
        host="https://your-arthur-engine-host.com",  # Optional if set in env var
        api_key="your-api-key"  # Optional if set in env var
    )

    # Create an AnyAgent instance with the Arthur tool
    agent = AnyAgent.create(
        "tinyagent",
        AgentConfig(
            model_id="gpt-4.1-nano",
            instructions="Use the arthur tool to validate the prompt and response before sending it to the LLM, and after the LLM has responded, use the arthur tool to validate the response",
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
