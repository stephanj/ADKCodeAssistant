"""
Planner agent for the Coding Assistant.

This module defines the planner agent for designing software features and components.
"""

from google.adk.agents import Agent
from google.genai.types import GenerateContentConfig

from coding_assistant.prompts.planner_agent import PLANNER_AGENT_PROMPT
from coding_assistant.tools.planning import generate_uml, create_task_list

# Planner agent for designing software features and components
planner_agent = Agent(
    model="gemini-2.0-flash-001",
    name="planner_agent",
    description="Plans software features, components, and architecture",
    instruction=PLANNER_AGENT_PROMPT,
    tools=[
        generate_uml,
        create_task_list,
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.2,
    ),
)
