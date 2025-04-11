"""
Coder agent for the Coding Assistant.

This module defines the coder agent for generating code implementations.
"""

from google.adk.agents import Agent
from google.genai.types import GenerateContentConfig

from coding_assistant.prompts.coder_agent import CODER_AGENT_PROMPT
from coding_assistant.tools.coding import generate_tests, refactor_code, create_project, create_file
from coding_assistant.tools.filesystem import search_files, read_file, list_directory, write_file

# Coder agent for generating code implementations
coder_agent = Agent(
    model="gemini-2.0-flash-001",
    name="coder_agent",
    description="Generates high-quality, working code implementations",
    instruction=CODER_AGENT_PROMPT,
    tools=[
        generate_tests,
        refactor_code,
        create_project,
        create_file,
        search_files,
        read_file,
        list_directory,
        write_file,
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.2,
    ),
)
