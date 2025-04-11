# Coding Assistant - An Agent-Based Development Helper

A powerful AI coding assistant built with Google's Agent Development Kit (ADK) that helps with code analysis, planning, implementation, and review.

## Overview

The Coding Assistant is an intelligent agent designed to enhance the software development workflow. It uses specialized sub-agents to tackle different aspects of development:

- **Analyzer Agent**: Understands and explains code structures and project architecture
- **Planner Agent**: Helps design and plan new features or components
- **Coder Agent**: Generates high-quality code implementations
- **Reviewer Agent**: Reviews code for bugs, best practices, and improvements

## Features

- 🔍 **Deep Code Analysis**: Understand complex codebases and their structures
- 📐 **Architecture Planning**: Get assistance with system design and component architecture
- 💻 **Smart Code Generation**: Generate working implementations with proper error handling
- 🔎 **Thorough Code Reviews**: Identify bugs, security issues, and improvement opportunities
- 📁 **File System Integration**: Seamlessly interacts with your project files

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Poetry package manager
- Google API key for accessing Gemini models

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/agenticCodingWithADK.git
   cd agenticCodingWithADK
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Create a `.env` file in the project root (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Running the Coding Assistant

There are several ways to run the Coding Assistant:

### Using the ADK CLI

```bash
# Run using the ADK CLI
adk run coding_assistant

# Or use the web interface
adk web
```

### Using the Python Module

```bash
# Run with a specific query
poetry run python -m coding_assistant.main "Analyze this project structure"

# Or run with the default query
poetry run python -m coding_assistant.main
```

### Programmatic Usage

```python
from coding_assistant.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.genai import types

# Set up services
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()

# Create a session with initial state
initial_state = {
    "project_path": "/path/to/your/project",
    "project_language": "python",
    "project_framework": "flask",
}

session = session_service.create_session(
    state=initial_state, app_name="coding_assistant", user_id="user1"
)

# Create a query
query = "Analyze the project structure"
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
        for part in event.content.parts:
            if hasattr(part, "text") and part.text:
                print(f"[{event.author}]: {part.text}")
```

## Example Queries

- "Analyze the structure and architecture of this project"
- "Help me plan a user authentication system with JWT"
- "Generate a Python function to parse and validate CSV files"
- "Review this code for performance issues and security vulnerabilities"
- "Explain how this algorithm works and suggest improvements"

## Project Structure

```
coding_assistant/
├── sub_agents/              # Specialized agent implementations
│   ├── analyzer/            # Code analysis agent
│   ├── planner/             # Feature planning agent
│   ├── coder/               # Code generation agent
│   └── reviewer/            # Code review agent
├── prompts/                 # Agent prompts and instructions
├── tools/                   # Tool implementations
│   ├── filesystem.py        # Filesystem interaction tools
│   ├── code_analysis.py     # Code analysis tools
│   ├── planning.py          # Planning tools
│   ├── coding.py            # Code generation tools
│   └── review.py            # Code review tools
├── shared_libraries/        # Shared functionality
│   ├── constants.py         # Constants and keys
│   └── types.py             # Type definitions using Pydantic
├── agent.py                 # Main agent definition
└── main.py                  # Command-line entry point
```

## Troubleshooting

### Common Issues

- **API Key Issues**: Ensure your Google API key is set correctly and has access to Gemini models
- **Import Errors**: Make sure you're using Poetry to manage dependencies
- **Module Not Found**: Verify that you have the `PYTHONPATH` environment variable set correctly

### Getting Help

If you encounter issues, please check the [Google ADK documentation](https://github.com/google/adk) or open an issue in this repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
