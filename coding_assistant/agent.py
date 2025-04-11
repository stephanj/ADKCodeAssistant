"""
Main agent for the Coding Assistant.

This module defines the root agent and sub-agents for the coding assistant.
"""

from google.adk.agents import Agent
from google.genai.types import GenerateContentConfig

from coding_assistant.sub_agents.analyzer.agent import analyzer_agent
from coding_assistant.sub_agents.planner.agent import planner_agent
from coding_assistant.sub_agents.coder.agent import coder_agent
from coding_assistant.sub_agents.reviewer.agent import reviewer_agent
from coding_assistant.tools.filesystem import load_initial_context
from coding_assistant.prompts.root_agent import ROOT_AGENT_PROMPT

# Root agent that orchestrates the coding assistant
root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="coding_assistant",
    description="A coding assistant that helps with code analysis, planning, implementation, and review",
    instruction=ROOT_AGENT_PROMPT,
    sub_agents=[
        analyzer_agent,
        planner_agent,
        coder_agent,
        reviewer_agent,
    ],
    before_agent_callback=load_initial_context,
    generate_content_config=GenerateContentConfig(
        temperature=0.2,
    ),
)
