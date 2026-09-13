# Import the AugmentedPromptAgent class
from workflow_agents.base_agents import AugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"

# Instantiate an object of AugmentedPromptAgent with the required parameters
augmented_agent = AugmentedPromptAgent(openai_api_key, persona)

# Send the prompt to the agent and store the response
augmented_agent_response = augmented_agent.respond(prompt)

# Print the agent's response
print(augmented_agent_response)

# Explanation:
# - What knowledge the agent likely used: the model's own general knowledge from its
#   training data (world geography — the fact that Paris is the capital of France).
#   No knowledge was provided by us; this agent has a persona but no knowledge attribute.
# - How the system prompt affected the response: the persona changed the FORM of the
#   answer, not its content. The system prompt instructed the model to answer as a
#   college professor whose answers begin with "Dear students," so the same fact
#   (Paris) is delivered in a lecturing register with that greeting. The
#   "Forget all previous context" instruction ensures the persona applies cleanly,
#   unaffected by any prior conversation state.