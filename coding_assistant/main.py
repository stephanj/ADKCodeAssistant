"""
Main entrypoint for the Coding Assistant.

This module demonstrates how to use the Coding Assistant agent.
"""

import os
import json
from dotenv import load_dotenv
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from coding_assistant.agent import root_agent

def run_coding_assistant(query: str):
    """
    Run the coding assistant with a query.
    
    Args:
        query: The query to run
    """
    # Load environment variables
    load_dotenv()
    
    # Set up services
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    
    # Create a session with initial state
    initial_state = {
        "project_path": os.getcwd(),
        "project_language": "python",
        "project_framework": "google-adk",
    }
    
    session = session_service.create_session(
        state=initial_state, app_name="coding_assistant", user_id="user1"
    )
    
    # Create content from query
    print(f"[User]: {query}")
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    # Create a runner
    runner = Runner(
        app_name="coding_assistant",
        agent=root_agent,
        artifact_service=artifact_service,
        session_service=session_service,
    )
    
    # Run the agent
    for event in runner.run(
        session_id=session.id, user_id="user1", new_message=content
    ):
        if event.content:
            author = event.author
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print(f"[{author}]: {part.text}")
                elif hasattr(part, "function_call"):
                    function_call = part.function_call
                    print(f"[{author}]: Function call: {function_call.name}({json.dumps(function_call.args)})")
                elif hasattr(part, "function_response"):
                    function_response = part.function_response
                    print(f"[{author}]: Function response: {function_response.name} -> {json.dumps(function_response.response)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = "Analyze the structure of this project"
    run_coding_assistant(query)
