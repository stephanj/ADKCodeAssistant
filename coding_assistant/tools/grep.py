"""
Grep tools for the Coding Assistant.

This module provides tools for searching text patterns in files.
"""

from google.adk.tools import ToolContext

def grep_files(directory: str, pattern: str, file_extension: str = "", context_lines: int = 0, tool_context: ToolContext = None) -> dict:
    """
    Search for text patterns within files. Returns matching files with line numbers and snippets.
    Similar to the Unix 'grep' command but optimized for code review.
    
    Args:
        directory: The base directory to search in
        pattern: The pattern to search for in file contents
        file_extension: Optional file extension to filter files (e.g., '.py', '.java'). Use empty string to search all files.
        context_lines: Number of context lines to include before/after matches
        tool_context: The tool context
        
    Returns:
        A dictionary containing matches found in files
    """
    import os
    import re
    
    try:
        results = []
        file_count = 0
        match_count = 0
        
        # Walk through the directory
        for root, _, files in os.walk(directory):
            for filename in files:
                # Skip non-matching extensions if specified
                if file_extension != "" and not filename.endswith(file_extension):
                    continue
                    
                file_path = os.path.join(root, filename)
                
                # Skip binary files
                try:
                    # Try to read as text
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    file_matches = []
                    
                    # Search for the pattern in each line
                    for i, line in enumerate(lines):
                        if re.search(pattern, line):
                            # Calculate context line boundaries
                            start = max(0, i - context_lines)
                            end = min(len(lines), i + context_lines + 1)
                            
                            # Add match with context
                            file_matches.append({
                                "line_number": i + 1,
                                "match": line.strip(),
                                "context": {
                                    "before": [lines[j].strip() for j in range(start, i)],
                                    "after": [lines[j].strip() for j in range(i + 1, end)]
                                }
                            })
                            match_count += 1
                    
                    if file_matches:
                        file_count += 1
                        results.append({
                            "file": file_path,
                            "matches": file_matches
                        })
                        
                except UnicodeDecodeError:
                    # Skip binary files
                    continue
                except Exception as e:
                    # Skip files with access issues
                    continue
        
        return {
            "success": True,
            "pattern": pattern,
            "directory": directory,
            "file_matches": results,
            "files_with_matches": file_count,
            "total_matches": match_count
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
