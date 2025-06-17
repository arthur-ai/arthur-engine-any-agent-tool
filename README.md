# arthur-engine-any-agent-tool

A tool that integrates Arthur Engine's guardrails with the Mozilla [any-agent](https://mozilla-ai.github.io/any-agent/) framework. This tool allows you to validate both prompts and responses against Arthur Engine's safety and content policies before they are processed or returned to users.

## Overview

The Arthur Tool provides a way to:
- Validate user prompts against safety and content policies
- Validate AI responses before they are returned to users
- Ensure compliance with Arthur Engine's guardrails throughout the conversation

## Prerequisites

1. Create an Arthur AI Account
   - Sign up at https://platform.arthur.ai/signup
   - Complete the registration process

2. Set Up Arthur Engine
   - Log into your Arthur AI account
   - Create a new GenAI model in the Arthur platform
   - Configure your desired guardrails and policies
   - Note down your:
     - Arthur Engine URL
     - API Key
     - Task ID (created when setting up your model)

3. Set Up OpenAI API Key
   - Create an account at https://platform.openai.com/signup if you haven't already
   - Generate an API key from https://platform.openai.com/api-keys
   - Set the environment variable:
     ```bash
     export OPENAI_API_KEY="your_openai_api_key"
     ```

4. Environment Variables
   Set the following environment variables:
   ```bash
   export ARTHUR_ENGINE_URL="your_engine_url"
   export ARTHUR_API_KEY="your_api_key"
   export ARTHUR_TASK_ID="your_task_id"
   export OPENAI_API_KEY="your_openai_api_key"
   ```

## Running the Example

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/arthur-engine-any-agent-tool.git
   cd arthur-engine-any-agent-tool
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the example agent:
   ```bash
   python examples/agent.py
   ```

The example agent will:
- Initialize the Arthur Tool with your credentials
- Create an AnyAgent instance with the tool configured
- Process a sample question ("What is the capital of France?")
- Validate both the question and response through Arthur Engine
- Print the final response

You can modify the example by changing the prompt in `examples/agent.py` to test different questions and see how the validation works.

## Usage Example

Here's a basic example of how to use the Arthur Tool with AnyAgent:

```python
from any_agent import AnyAgent, AgentConfig
from src.tools import ArthurTool
import uuid

# Initialize the Arthur tool
arthur_tool = ArthurTool(
    task_id=ARTHUR_TASK_ID,
    conversation_id=str(uuid.uuid4()),  # Generate a unique conversation ID
    user_id=str(uuid.uuid4()),          # Generate a unique user ID
    host=ARTHUR_ENGINE_URL,
    api_key=ARTHUR_API_KEY,
)

# Create an AnyAgent instance with the Arthur tool
agent = AnyAgent.create(
    "tinyagent",
    AgentConfig(
        model_id="gpt-4.1",
        instructions="""You are an agent that helps users answer questions. 
        
        When a user asks a question, first validate their question is allowed by passing it to the prompt argument of the arthur_tool.
        
        If the question fails any of the checks, respond to the user with a helpful message saying you can't answer their question because it violates content policies.
        
        After verifying the user's question is valid, verify your answer is valid by passing it as the response argument of the arthur tool. 
        
        Generate new responses until it passes all validation checks, then respond to the user.""",
        tools=[arthur_tool],
    )
)

# Use the agent
response = agent.run("What is the capital of France?")
```

## Example Trace

Here's an example of how the tool validates prompts and responses:

```
╭───────────────────────────── CALL_LLM: gpt-4.1 ──────────────────────────────╮
│ ╭─ INPUT ──────────────────────────────────────────────────────────────────╮ │
│ │ [                                                                        │ │
│ │   {                                                                      │ │
│ │     "role": "system",                                                    │ │
│ │     "content": "You are an agent that helps users answer questions. \n   │ │
│ │   },                                                                     │ │
│ │   {                                                                      │ │
│ │     "role": "user",                                                      │ │
│ │     "content": "What is the capital of france?"                          │ │
│ │   }                                                                      │ │
│ │ ]                                                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
│ ╭─ OUTPUT ─────────────────────────────────────────────────────────────────╮ │
│ │ [                                                                        │ │
│ │   {                                                                      │ │
│ │     "tool.name": "wrapped_function",                                     │ │
│ │     "tool.args": "{\"prompt\":\"What is the capital of france?\"}"       │ │
│ │   }                                                                      │ │
│ │ ]                                                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
│ ╭─ USAGE ──────────────────────────────────────────────────────────────────╮ │
│ │ {                                                                        │ │
│ │   "input_tokens": 460,                                                   │ │
│ │   "output_tokens": 21                                                    │ │
│ │ }                                                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────── EXECUTE_TOOL: wrapped_function ───────────────────────╮
│ ╭─ Input ──────────────────────────────────────────────────────────────────╮ │
│ │ {                                                                        │ │
│ │   "prompt": "What is the capital of france?"                             │ │
│ │ }                                                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
│ ╭─ OUTPUT ─────────────────────────────────────────────────────────────────╮ │
│ │ {'inference_id': '9e14d766-41d5-4884-9417-a294db0b8951', 'rule_results': │ │
│ │ [{'id': '5e4003f1-a951-41d0-86d7-08f35031d415', 'name': 'Prompt          │ │
│ │ Injection', 'rule_type': 'PromptInjectionRule', 'scope': 'task',         │ │
│ │ 'result': 'Pass', 'latency_ms': 125, 'details': None}, {'id':            │ │
│ │ '335e1497-e2c8-44a6-a4b2-88cd63caf791', 'name': 'Toxicity', 'rule_type': │ │
│ │ 'ToxicityRule', 'scope': 'task', 'result': 'Pass', 'latency_ms': 54,     │ │
│ │ 'details': {'score': None, 'message': 'No toxicity detected!',           │ │
│ │ 'toxicity_score': 4.757278293254785e-05, 'toxicity_violation_type':      │ │
│ │ 'benign'}}], 'user_id': '2dbde4b4-1e78-4784-ae82-6f79c498a66b'}          │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
╰──────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────── CALL_LLM: gpt-4.1 ──────────────────────────────╮
│ ╭─ OUTPUT ─────────────────────────────────────────────────────────────────╮ │
│ │ [                                                                        │ │
│ │   {                                                                      │ │
│ │     "tool.name": "wrapped_function",                                     │ │
│ │     "tool.args": "{\"prompt\":\"What is the capital of france?\",\"respo │ │
│ │   }                                                                      │ │
│ │ ]                                                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
│ ╭─ USAGE ──────────────────────────────────────────────────────────────────╮ │
│ │ {                                                                        │ │
│ │   "input_tokens": 732,                                                   │ │
│ │   "output_tokens": 31                                                    │ │
│ │ }                                                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────── EXECUTE_TOOL: wrapped_function ───────────────────────╮
│ ╭─ Input ──────────────────────────────────────────────────────────────────╮ │
│ │ {                                                                        │ │
│ │   "prompt": "What is the capital of france?",                            │ │
│ │   "response": "The capital of France is Paris."                          │ │
│ │ }                                                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
│ ╭─ OUTPUT ─────────────────────────────────────────────────────────────────╮ │
│ │ {'inference_id': '3d304f02-289d-4a74-8239-db776c0e14dc', 'rule_results': │ │
│ │ [{'id': '335e1497-e2c8-44a6-a4b2-88cd63caf791', 'name': 'Toxicity',      │ │
│ │ 'rule_type': 'ToxicityRule', 'scope': 'task', 'result': 'Pass',          │ │
│ │ 'latency_ms': 27, 'details': {'score': None, 'message': 'No toxicity     │ │
│ │ detected!', 'toxicity_score': 6.224388198461384e-05,                     │ │
│ │ 'toxicity_violation_type': 'benign'}}], 'user_id': None}                 │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
╰──────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────── CALL_LLM: gpt-4.1 ──────────────────────────────╮
│ ╭─ OUTPUT ─────────────────────────────────────────────────────────────────╮ │
│ │ The capital of France is Paris.                                          │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
│ ╭─ USAGE ──────────────────────────────────────────────────────────────────╮ │
│ │ {                                                                        │ │
│ │   "input_tokens": 920,                                                   │ │
│ │   "output_tokens": 8                                                     │ │
│ │ }                                                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
╰──────────────────────────────────────────────────────────────────────────────