# Test script for DirectPromptAgent class

from workflow_agents.base_agents import DirectPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the Capital of France?"

# Instantiate the DirectPromptAgent as direct_agent
direct_agent = DirectPromptAgent(openai_api_key)

# Use direct_agent to send the prompt and store the response
direct_agent_response = direct_agent.respond(prompt)

# Print the response from the agent
print(direct_agent_response)

# Explanatory message describing the knowledge source used by the agent
print("Knowledge source: The DirectPromptAgent used only the LLM's own general knowledge "
      "acquired during training to answer this prompt. No system prompt, persona, or "
      "external knowledge was provided — the response reflects the model's raw, "
      "unsteered behavior.")