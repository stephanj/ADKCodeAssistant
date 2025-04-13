"""
Filesystem tools for the Coding Assistant.

This module provides tools for interacting with the filesystem to read code and project structures.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

# Removed the DEFAULT_CONTEXT_PATH limitation for senior developers
# to allow full filesystem access

def search_files(path: str, pattern: str, tool_context: ToolContext) -> dict:
    """
    Search for files matching a pattern in a given path.
    
    Args:
        path: The path to search in
        pattern: The pattern to search for
        tool_context: The tool context
        
    Returns:
        A dictionary containing the matching files
    """
    import os
    import fnmatch
    
    matching_files = []
    
    try:
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, f"*{pattern}*"):
                file_path = os.path.join(root, filename)
                matching_files.append({
                    "path": file_path,
                    "name": filename,
                    "type": "file"
                })
            
            # Also match directory names if needed
            for dirname in fnmatch.filter(dirnames, f"*{pattern}*"):
                dir_path = os.path.join(root, dirname)
                matching_files.append({
                    "path": dir_path,
                    "name": dirname,
                    "type": "directory"
                })
        
        return {
            "success": True,
            "path": path,
            "pattern": pattern,
            "matches": matching_files,
            "count": len(matching_files)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def read_file(path: str, tool_context: ToolContext) -> dict:
    """
    Read the contents of a file.
    
    Args:
        path: The path to the file to read
        tool_context: The tool context
        
    Returns:
        A dictionary containing the file contents
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "success": True,
            "path": path,
            "content": content,
            "size": len(content)
        }
    except UnicodeDecodeError:
        # Try reading as binary if text reading fails
        try:
            with open(path, 'rb') as f:
                content = f.read()
            return {
                "success": True,
                "path": path,
                "is_binary": True,
                "message": "This appears to be a binary file",
                "size": len(content)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read binary file: {str(e)}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def list_directory(path: str, tool_context: ToolContext) -> dict:
    """
    List the contents of a directory.
    
    Args:
        path: The path to the directory to list
        tool_context: The tool context
        
    Returns:
        A dictionary containing the directory contents
    """
    import os
    from datetime import datetime
    
    try:
        # Get all entries in the directory
        entries = []
        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)
            
            # Get info about the entry
            stats = os.stat(entry_path)
            
            entry_info = {
                "name": entry,
                "path": entry_path,
                "lastModified": int(stats.st_mtime * 1000)  # Convert to milliseconds
            }
            
            # Add type and size info
            if os.path.isdir(entry_path):
                entry_info["type"] = "DIR"
            else:
                entry_info["type"] = "FILE"
                entry_info["size"] = stats.st_size
                
            entries.append(entry_info)
            
        return {
            "success": True,
            "path": path,
            "entries": entries,
            "count": len(entries)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def write_file(path: str, content: str, tool_context: ToolContext) -> dict:
    """
    Write content to a file.
    
    Args:
        path: The path to the file to write
        content: The content to write to the file
        tool_context: The tool context
        
    Returns:
        A dictionary indicating success or failure
    """
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write the content to the file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return {
            "success": True,
            "path": path,
            "message": f"Successfully wrote {len(content)} characters to {path}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def _set_initial_states(source: Dict[str, Any], target: State | dict[str, Any]):
    """
    Set the initial session state.
    
    Args:
        source: A JSON object of states
        target: The session state to update
    """
    # Set system time
    if "system_time" not in target:
        target["system_time"] = str(datetime.now())
    
    # Set context_loaded flag
    if "context_loaded" not in target:
        target["context_loaded"] = True
        
    # Update with source data
    target.update(source)
    
    # Set default values for required template variables if they don't exist
    if "project_path" not in target:
        target["project_path"] = os.getcwd()
        
    if "project_language" not in target:
        target["project_language"] = "python"
        
    if "project_framework" not in target:
        target["project_framework"] = "unknown"

def load_initial_context(callback_context: CallbackContext):
    """
    Load initial context for the coding assistant.
    
    Args:
        callback_context: The callback context
    """
    # Initialize with basic state, allowing senior developers to specify their own context
    # via environment variables or explicit inputs
    data = {"state": {
        "project_path": os.getcwd(),
        "project_language": "python",
        "project_framework": "unknown",
    }}
    
    # Check for optional context file path in environment
    context_path = os.getenv("CODING_ASSISTANT_CONTEXT", "")
    if context_path and os.path.exists(context_path):
        try:
            with open(context_path, "r") as file:
                context_data = json.load(file)
                data = context_data
                print(f"\nLoaded context from {context_path}: {data}\n")
        except Exception as e:
            print(f"\nWarning: Failed to load context from {context_path}: {str(e)}\n")
    
    _set_initial_states(data.get("state", {}), callback_context.state)

def memorize(key: str, value: str, tool_context: ToolContext):
    """
    Store information in the session state.
    
    Args:
        key: The key to store the value under
        value: The value to store
        tool_context: The tool context
        
    Returns:
        A status message
    """
    tool_context.state[key] = value
    return {"status": f'Stored "{key}": "{value}"'}