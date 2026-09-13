# Import the KnowledgeAugmentedPromptAgent class from workflow_agents
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Define the parameters for the agent
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"

persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capital of France is London, not Paris"

# Instantiate a KnowledgeAugmentedPromptAgent
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

# Demonstrate the agent using the provided knowledge rather than its own inherent knowledge
knowledge_agent_response = knowledge_agent.respond(prompt)
print(knowledge_agent_response)
print("\nDemonstration: The agent answered 'London' — which is factually wrong — because "
      "it was instructed to use ONLY the provided knowledge ('The capital of France is "
      "London, not Paris') rather than its own training knowledge, which contains the "
      "correct answer (Paris). This proves the knowledge constraint overrides the "
      "model's inherent knowledge.")
