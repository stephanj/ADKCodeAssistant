"""
Planner agent for the Coding Assistant.

This module defines the planner agent for designing software features and components.
"""

from google.adk.agents import Agent
from google.genai.types import GenerateContentConfig

from coding_assistant.prompts.planner_agent import PLANNER_AGENT_PROMPT
from coding_assistant.tools.planning import create_task_list
from coding_assistant.tools.filesystem import search_files, read_file, list_directory
from coding_assistant.tools.github_tools import github_search_code, github_list_directory_contents, github_get_file_contents

# Planner agent for designing software features and components
planner_agent = Agent(
    model="gemini-2.0-flash-001",
    name="planner_agent",
    description="Plans software features, components, and architecture",
    instruction=PLANNER_AGENT_PROMPT,
    tools=[
        create_task_list,
        search_files,
        read_file,
        list_directory,

        github_get_file_contents,
        github_list_directory_contents,
        github_search_code
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.2,
    ),
)
