# agentic_workflow.py

# Import the agents from the workflow_agents library
from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent
import os
from dotenv import load_dotenv

# Load environment variables and the OpenAI key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Load the product spec
with open("Product-Spec-Email-Router.txt", "r") as file:
    product_spec = file.read()

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
knowledge_action_planning = knowledge_action_planning + "\nThe steps to create a development plan are always exactly these three, returned as a numbered list: 1. Define user stories for the product. 2. Define features for the product by grouping user stories. 3. Define development tasks for the product."
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
)
knowledge_product_manager = knowledge_product_manager + product_spec
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_product_manager, knowledge_product_manager)

# Product Manager - Evaluation Agent
persona_product_manager_eval = "You are an evaluation agent that checks the answers of other worker agents"
evaluation_criteria_product_manager = "The answer should be stories that follow the following structure: As a [type of user], I want [an action or feature] so that [benefit/value]."
product_manager_evaluation_agent = EvaluationAgent(openai_api_key, persona_product_manager_eval, evaluation_criteria_product_manager, product_manager_knowledge_agent, 10)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
knowledge_program_manager = knowledge_program_manager + "\nAlways write the actual features (not advice about features), each using exactly this structure: Feature Name:, Description:, Key Functionality:, User Benefit:."
knowledge_program_manager = knowledge_program_manager + "\nThe features must be for the product described in this specification:\n" + product_spec
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_program_manager, knowledge_program_manager)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria_program_manager = "The answer should be product features that follow the following structure: " \
                     "Feature Name: A clear, concise title that identifies the capability\n" \
                     "Description: A brief explanation of what the feature does and its purpose\n" \
                     "Key Functionality: The specific capabilities or actions the feature provides\n" \
                     "User Benefit: How this feature creates value for the user"
program_manager_evaluation_agent = EvaluationAgent(openai_api_key, persona_program_manager_eval, evaluation_criteria_program_manager, program_manager_knowledge_agent, 10)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
knowledge_dev_engineer = knowledge_dev_engineer + "\nAlways write the actual tasks (not advice about tasks), each using exactly this structure: Task ID:, Task Title:, Related User Story:, Description:, Acceptance Criteria:, Estimated Effort:, Dependencies:."
knowledge_dev_engineer = knowledge_dev_engineer + "\nThe tasks must be for the product described in this specification:\n" + product_spec
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_dev_engineer, knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria_dev_engineer = "The answer should be tasks following this exact structure: " \
                     "Task ID: A unique identifier for tracking purposes\n" \
                     "Task Title: Brief description of the specific development work\n" \
                     "Related User Story: Reference to the parent user story\n" \
                     "Description: Detailed explanation of the technical work required\n" \
                     "Acceptance Criteria: Specific requirements that must be met for completion\n" \
                     "Estimated Effort: Time or complexity estimation\n" \
                     "Dependencies: Any tasks that must be completed first"
development_engineer_evaluation_agent = EvaluationAgent(openai_api_key, persona_dev_engineer_eval, evaluation_criteria_dev_engineer, development_engineer_knowledge_agent, 10)


# Job function persona support functions
def product_manager_support_function(query):
    response = product_manager_knowledge_agent.respond(query)
    result = product_manager_evaluation_agent.evaluate(response)
    return result["final_response"]


def program_manager_support_function(query):
    response = program_manager_knowledge_agent.respond(query)
    result = program_manager_evaluation_agent.evaluate(response)
    return result["final_response"]


def development_engineer_support_function(query):
    response = development_engineer_knowledge_agent.respond(query)
    result = development_engineer_evaluation_agent.evaluate(response)
    return result["final_response"]


# Routing Agent
routing_agent = RoutingAgent(openai_api_key, {})
agents = [
    {
        "name": "Product Manager",
        "description": "Define user stories for the product. A user story describes a persona, an action, and a benefit from the product specification",
        "func": lambda x: product_manager_support_function(x)
    },
    {
        "name": "Program Manager",
        "description": "Responsible for defining product features by grouping and organizing stories into cohesive feature groups. Does not write stories or define engineering tasks",
        "func": lambda x: program_manager_support_function(x)
    },
    {
        "name": "Development Engineer",
        "description": "Responsible for defining detailed engineering development tasks for implementing user stories. Does not write user stories or define features",
        "func": lambda x: development_engineer_support_function(x)
    }
]
routing_agent.agents = agents

# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
workflow_prompt = "What would the development tasks for this product be?"
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")

workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)

completed_steps = []

for step in workflow_steps:
    print(f"\nExecuting step: {step}")
    result = routing_agent.route(step)
    completed_steps.append(result)
    print(f"Step result:\n{result}")

print("\n*** Final output of the workflow ***\n")
final_report = f"""# Email Router Project Plan

## User Stories
{completed_steps[0]}

## Product Features
{completed_steps[1]}

## Engineering Tasks
{completed_steps[2]}
"""
print(final_report)