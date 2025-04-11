"""
Reviewer agent for the Coding Assistant.

This module defines the reviewer agent for reviewing code quality and identifying improvements.
"""

from google.adk.agents import Agent
from google.genai.types import GenerateContentConfig

from coding_assistant.prompts.reviewer_agent import REVIEWER_AGENT_PROMPT
from coding_assistant.tools.review import check_best_practices, security_scan

# Reviewer agent for reviewing code quality and identifying improvements
reviewer_agent = Agent(
    model="gemini-2.0-flash-001",
    name="reviewer_agent",
    description="Reviews code for quality, bugs, and improvements",
    instruction=REVIEWER_AGENT_PROMPT,
    tools=[
        check_best_practices,
        security_scan,
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.1,
    ),
)
