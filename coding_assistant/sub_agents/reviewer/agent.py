"""
Reviewer agent for the Coding Assistant.

This module defines the reviewer agent for reviewing code quality and identifying improvements.
"""

from google.adk.agents import Agent
from google.genai.types import GenerateContentConfig

from coding_assistant.prompts.reviewer_agent import REVIEWER_AGENT_PROMPT
from coding_assistant.tools.review import check_best_practices, security_scan
from coding_assistant.tools.filesystem import search_files, read_file, list_directory
from coding_assistant.tools.grep import grep_files
from coding_assistant.tools.github_tools import github_search_code, github_list_directory_contents, github_get_file_contents

# Reviewer agent for reviewing code quality and identifying improvements
reviewer_agent = Agent(
    model="gemini-2.0-flash-001",
    name="reviewer_agent",
    description="Reviews code for quality, bugs, and improvements",
    instruction=REVIEWER_AGENT_PROMPT,
    tools=[
        # Code review tools
        check_best_practices,
        security_scan,
        
        # File operation tools
        search_files,
        read_file,
        list_directory,
        grep_files,

        github_get_file_contents,
        github_list_directory_contents,
        github_search_code
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.1,
    ),
)
