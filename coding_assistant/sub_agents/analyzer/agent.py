"""
Analyzer agent for the Coding Assistant.

This module defines the analyzer agent for analyzing code and project structures.
"""

from google.adk.agents import Agent
from google.genai.types import GenerateContentConfig

from coding_assistant.prompts.analyzer_agent import ANALYZER_AGENT_PROMPT
from coding_assistant.tools.code_analysis import analyze_dependencies, analyze_complexity
from coding_assistant.tools.github_tools import github_search_code, github_list_directory_contents, github_get_file_contents

# Analyzer agent for understanding code and project structures
analyzer_agent = Agent(
    model="gemini-2.0-flash-001",
    name="analyzer_agent",
    description="Analyzes code and project structures to help understand existing codebases",
    instruction=ANALYZER_AGENT_PROMPT,
    tools=[
        analyze_dependencies,
        analyze_complexity,

        github_get_file_contents,
        github_list_directory_contents,
        github_search_code
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.1,
    ),
)
