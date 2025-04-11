# Coding Assistant Agent

An intelligent coding assistant built with Google's Agent Development Kit (ADK) that helps with code analysis, planning, implementation, and review.

## Overview

The Coding Assistant is a comprehensive AI agent designed to help developers with various aspects of the software development process. It consists of specialized sub-agents that each focus on different parts of the development workflow:

- **Analyzer Agent**: Helps understand existing code and project structures
- **Planner Agent**: Assists with designing and planning new features or components
- **Coder Agent**: Generates high-quality code implementations
- **Reviewer Agent**: Reviews code for bugs, best practices, and improvements

## Features

- **Code Analysis**: Understand complex codebases and their structures
- **Planning and Design**: Get help with architecture and component design
- **Code Generation**: Generate working implementations with proper error handling
- **Code Review**: Identify bugs, security issues, and improvement opportunities
- **File System Integration**: Interact with your project's files and directories

## Usage

```python
from coding_assistant.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.genai import types

# Set up services
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()

# Create a session
session = session_service.create_session(
    state={}, app_name="coding_assistant", user_id="user1"
)

# Create a query
query = "Can you help me analyze the structure of this project?"
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
```

## Example Queries

- "Analyze the structure of this project"
- "Help me plan a new user authentication feature"
- "Generate a function to parse CSV files"
- "Review this code for potential bugs and improvements"

## Requirements

- Python 3.9+
- Google Agent Development Kit
- Access to Gemini models via Google AI Studio or Vertex AI

## License

This project is licensed under the MIT License - see the LICENSE file for details.
