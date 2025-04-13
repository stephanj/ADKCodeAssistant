"""
GitHub tools for the Coding Assistant.

This module provides tools for GitHub repository content management operations.
"""

import base64
from typing import Dict, Optional, Any, Tuple
from google.adk.tools import ToolContext

# Try importing GitHub libraries
# First, check if PyGithub is available
try:
    import github
    from github import Github
    from github.Repository import Repository
    from github.ContentFile import ContentFile
    from github.GithubException import GithubException
    try:
        from github.GithubException import UnknownObjectException
    except ImportError:
        # In some versions, this might be in a different location
        UnknownObjectException = GithubException
    _GITHUB_AVAILABLE = True
    _USING_PYGITHUB = True
except ImportError:
    # PyGithub not available, try githubpy
    try:
        import githubpy
        _GITHUB_AVAILABLE = True
        _USING_PYGITHUB = False
    except ImportError:
        # No GitHub libraries available
        _GITHUB_AVAILABLE = False
        _USING_PYGITHUB = False


def _get_github_env() -> Tuple[bool, Dict[str, Any]]:
    """
    Get GitHub environment configuration.
    
    Returns:
        Tuple[bool, Dict[str, Any]]: A tuple with success status and environment data or error
    """
    # In a real implementation, this would get configuration from environment
    # or a config file. For now we'll return a placeholder.
    try:
        # This is a placeholder. In a real app, you'd get these from env vars or config
        import os
        token = os.environ.get("GITHUB_TOKEN")
        repo = os.environ.get("GITHUB_REPOSITORY")
        
        if not token:
            return False, {"error": "GitHub token not configured. Set GITHUB_TOKEN environment variable."}
        
        return True, {
            "token": token,
            "repository": repo
        }
    except Exception as e:
        return False, {"error": f"Failed to get GitHub environment: {str(e)}"}


def _create_github_client(env: Dict[str, Any]) -> Tuple[bool, Any]:
    """
    Create a GitHub client using the provided environment.
    
    Args:
        env: GitHub environment configuration
    
    Returns:
        Tuple[bool, Any]: A tuple with success status and GitHub client or error
    """
    # First check if any GitHub libraries are available
    if not globals().get('_GITHUB_AVAILABLE', False):
        return False, {"error": "No GitHub libraries available. Please install PyGithub with: pip install PyGithub"}
    
    try:
        token = env.get("token")
        if not token:
            return False, {"error": "GitHub token not provided"}
        
        # Check which GitHub library is available
        if globals().get('_USING_PYGITHUB', False):
            # Using PyGithub
            client = Github(token)
        else:
            # Using githubpy
            client = githubpy.Github(token)
        
        return True, client
    except Exception as e:
        return False, {"error": f"Failed to create GitHub client: {str(e)}"}



def _format_content_details(content) -> Dict[str, Any]:
    """
    Format GitHub content details into a consistent structure.
    This handles both PyGithub and githubpy response objects.
    
    Args:
        content: GitHub content object
    
    Returns:
        Dict[str, Any]: Formatted content details
    """
    result = {}
    
    # Safely get attributes that might differ between libraries
    for attr in ["name", "path", "sha", "size"]:
        try:
            result[attr] = getattr(content, attr)
        except (AttributeError, TypeError):
            # Handle case where the attribute doesn't exist
            result[attr] = f"unknown_{attr}"
    
    return result


def _success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a successful response.
    
    Args:
        data: Response data
    
    Returns:
        Dict[str, Any]: Formatted success response
    """
    return {
        "success": True,
        **data
    }


def _error_response(message: str) -> Dict[str, Any]:
    """
    Format an error response.
    
    Args:
        message: Error message
    
    Returns:
        Dict[str, Any]: Formatted error response
    """
    return {
        "success": False,
        "error": message
    }


def github_get_file_contents(
    path: str,
    repository: Optional[str] = None,
    ref: Optional[str] = None,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Get the contents of a file in a GitHub repository.
    Returns the file content and metadata such as size and sha.
    
    Args:
        path: Path to the file in the GitHub repository (relative to repo root, e.g., 'src/main/java/file.java')
        repository: The GitHub repository name in format 'owner/repo'
        ref: Branch or commit SHA (defaults to the default branch)
        tool_context: The tool context
    
    Returns:
        Dict[str, Any]: A dictionary containing file content and metadata or error
    """
    # Check if GitHub is available first
    if not globals().get('_GITHUB_AVAILABLE', False):
        return _error_response("GitHub functionality is not available. Please install PyGithub with: pip install PyGithub")
        
    if not path:
        return _error_response("File path is required")
    
    # Normalize path - convert any absolute paths to relative (remove leading slashes)
    normalized_path = path.lstrip('/')
    
    success, env = _get_github_env()
    if not success:
        return _error_response(env["error"])
    
    success, github_client = _create_github_client(env)
    if not success:
        return _error_response(github_client["error"])
    
    # Use provided repository or default from environment
    repo_name = repository if repository else env.get("repository")
    if not repo_name:
        return _error_response("Repository name is required")
    
    try:
        repo = github_client.get_repo(repo_name)
        
        # Get contents, using ref if provided
        try:
            if ref:
                content = repo.get_contents(normalized_path, ref=ref)
            else:
                content = repo.get_contents(normalized_path)
        except UnknownObjectException:
            # File not found - provide a clearer error message
            return _error_response(f"File not found in repository: {normalized_path}")
        except Exception as e:
            # Handle other API exceptions
            return _error_response(f"Error accessing file {normalized_path}: {str(e)}")
        
        # Check if it's a file (not a directory)
        if isinstance(content, list):
            return _error_response("Path points to a directory, not a file")
        
        # Get content details
        content_data = _format_content_details(content)
        content_data["type"] = "file"
        
        # Safely get URL attributes that might differ between libraries
        try:
            content_data["url"] = content.html_url
        except (AttributeError, TypeError):
            try:
                content_data["url"] = content.url
            except (AttributeError, TypeError):
                content_data["url"] = "unknown_url"
                
        try:
            content_data["download_url"] = content.download_url
        except (AttributeError, TypeError):
            content_data["download_url"] = "unknown_download_url"
        
        # Get and decode content
        try:
            if hasattr(content, 'content') and content.content:
                # The content is base64 encoded
                try:
                    decoded_content = base64.b64decode(content.content).decode('utf-8')
                    content_data["content"] = decoded_content
                except Exception as e:
                    content_data["content"] = f"[Content decoding failed: {str(e)}]"
            else:
                content_data["content"] = ""
        except (AttributeError, TypeError) as e:
            content_data["content"] = f"[Content access error: {str(e)}]"
        
        return _success_response({"file": content_data})
        
    except UnknownObjectException:
        return _error_response(f"Repository not found: {repo_name}")
    except Exception as e:
        return _error_response(f"Unexpected error: {str(e)}")


def github_list_directory_contents(
    repository: Optional[str] = None,
    path: Optional[str] = None,
    ref: Optional[str] = None,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    List contents of a directory in a GitHub repository.
    Returns a list of files and directories at the specified GitHub path.
    
    Args:
        repository: The GitHub repository name in format 'owner/repo'
        path: Path to the directory in the GitHub repository (use '/' for root)
        ref: Branch or commit SHA (defaults to the default branch)
        tool_context: The tool context
    
    Returns:
        Dict[str, Any]: A dictionary containing directory contents or error
    """
    # Check if GitHub is available first
    if not globals().get('_GITHUB_AVAILABLE', False):
        return _error_response("GitHub functionality is not available. Please install PyGithub with: pip install PyGithub")
        
    success, env = _get_github_env()
    if not success:
        return _error_response(env["error"])
    
    success, github_client = _create_github_client(env)
    if not success:
        return _error_response(github_client["error"])
    
    # Use provided repository or default from environment
    repo_name = repository if repository else env.get("repository")
    if not repo_name:
        return _error_response("Repository name is required")
    
    # Normalize path - convert any absolute paths to relative (remove leading slashes)
    dir_path = path.lstrip('/') if path else ""
    
    try:
        repo = github_client.get_repo(repo_name)
        
        # Get contents, using ref if provided
        try:
            if ref:
                contents = repo.get_contents(dir_path, ref=ref)
            else:
                contents = repo.get_contents(dir_path)
        except UnknownObjectException:
            # Directory not found - provide a clearer error message
            return _error_response(f"Directory not found in repository: {dir_path}")
        except Exception as e:
            # Handle other API exceptions
            return _error_response(f"Error accessing directory {dir_path}: {str(e)}")
        
        # Ensure contents is a list, as it might be a single ContentFile for files
        if not isinstance(contents, list):
            return _error_response(f"Path '{dir_path}' points to a file, not a directory")
        
        contents_list = []
        
        for content in contents:
            content_data = _format_content_details(content)
            content_data["type"] = "directory" if isinstance(content, list) else "file"
            
            # Safely get URL attributes
            try:
                content_data["url"] = content.html_url
            except (AttributeError, TypeError):
                try:
                    content_data["url"] = content.url
                except (AttributeError, TypeError):
                    content_data["url"] = "unknown_url"
            
            # Add download URL for files
            if content_data["type"] == "file":
                try:
                    content_data["download_url"] = content.download_url
                except (AttributeError, TypeError):
                    content_data["download_url"] = "unknown_download_url"
            
            contents_list.append(content_data)
        
        return _success_response({
            "contents": contents_list,
            "path": dir_path
        })
        
    except UnknownObjectException:
        return _error_response(f"Repository not found: {repo_name}")
    except Exception as e:
        return _error_response(f"Unexpected error: {str(e)}")


# def create_or_update_github_file(
#     path: str,
#     content: str,
#     message: str,
#     repository: Optional[str] = None,
#     branch: Optional[str] = None,
#     sha: Optional[str] = None,
#     tool_context: ToolContext = None
# ) -> Dict[str, Any]:
#     """
#     Create or update a file in a repository.
#     If the file doesn't exist, it will be created. If it exists, it will be updated.
#
#     Args:
#         path: Path to the file in the repository
#         content: File content
#         message: Commit message
#         repository: Repository name in format 'owner/repo'
#         branch: Branch name (defaults to the default branch)
#         sha: Current file SHA (required for updates, not for new files)
#         tool_context: The tool context
#
#     Returns:
#         Dict[str, Any]: A dictionary containing operation result or error
#     """
#     if not path:
#         return _error_response("File path is required")
#
#     if content is None:
#         return _error_response("File content is required")
#
#     if not message:
#         return _error_response("Commit message is required")
#
#     success, env = _get_github_env()
#     if not success:
#         return _error_response(env["error"])
#
#     success, github_client = _create_github_client(env)
#     if not success:
#         return _error_response(github_client["error"])
#
#     # Use provided repository or default from environment
#     repo_name = repository if repository else env.get("repository")
#     if not repo_name:
#         return _error_response("Repository name is required")
#
#     try:
#         repo = github_client.get_repo(repo_name)
#
#         # Determine branch to use
#         branch_to_use = branch if branch else repo.default_branch
#
#         # Create or update file
#         response = repo.update_file(
#             path=path,
#             message=message,
#             content=content,
#             sha=sha,
#             branch=branch_to_use
#         ) if sha else repo.create_file(
#             path=path,
#             message=message,
#             content=content,
#             branch=branch_to_use
#         )
#
#         # Prepare response data
#         content_data = {"path": path}
#
#         # Get the commit info
#         commit = response["commit"]
#         commit_data = {
#             "sha": commit.sha,
#             "url": commit.html_url,
#             "message": commit.commit.message
#         }
#         content_data["commit"] = commit_data
#
#         # Get the content info
#         file_content = response["content"]
#         content_data["sha"] = file_content.sha
#         content_data["name"] = file_content.name
#         content_data["url"] = file_content.html_url
#
#         return _success_response({
#             "operation": "update" if sha else "create",
#             "file": content_data
#         })
#
#     except UnknownObjectException:
#         return _error_response("Repository not found")
#     except Exception as e:
#         return _error_response(f"Unexpected error: {str(e)}")


def github_search_code(
    query: str,
    repository: Optional[str] = None,
    extension: Optional[str] = None,
    limit: Optional[int] = None,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Search for code within GitHub repositories.
    Searches GitHub for code matching the query.
    
    Args:
        query: Search query
        repository: The GitHub repository name in format 'owner/repo' to limit search
        extension: Filter by file extension (e.g., 'java', 'py')
        limit: Maximum number of results to return
        tool_context: The tool context
    
    Returns:
        Dict[str, Any]: A dictionary containing search results or error
    """
    if not query:
        return _error_response("Search query is required")
    
    success, env = _get_github_env()
    if not success:
        return _error_response(env["error"])
    
    success, github_client = _create_github_client(env)
    if not success:
        return _error_response(github_client["error"])
    
    try:
        # Build search query
        query_builder = query
        
        # Add repository filter if provided
        if repository:
            query_builder += f" repo:{repository}"
        
        # Add extension filter if provided
        if extension:
            query_builder += f" extension:{extension}"
        
        actual_limit = limit if limit and limit > 0 else 20  # Default to 20 results
        
        # Search for code
        code_search = github_client.search_code(query_builder)
        
        results_list = []
        count = 0
        
        for content in code_search[:actual_limit]:
            if count >= actual_limit:
                break
            
            # Use safe attribute access
            content_data = {}
            
            # Basic metadata
            for attr in ["name", "path", "sha"]:
                try:
                    content_data[attr] = getattr(content, attr)
                except (AttributeError, TypeError):
                    content_data[attr] = f"unknown_{attr}"
                    
            # Repository info
            try:
                content_data["repository"] = content.repository.full_name
            except (AttributeError, TypeError):
                try:
                    content_data["repository"] = str(content.repository)
                except (AttributeError, TypeError):
                    content_data["repository"] = "unknown_repository"
                    
            # URL info
            try:
                content_data["html_url"] = content.html_url
            except (AttributeError, TypeError):
                try:
                    content_data["html_url"] = content.url
                except (AttributeError, TypeError):
                    content_data["html_url"] = "unknown_url"
            
            # Try to get a snippet of content for context
            try:
                file_content = content.decoded_content.decode('utf-8')
                
                # Get a snippet (first 200 chars or less)
                snippet_length = min(len(file_content), 200)
                snippet = file_content[:snippet_length]
                if snippet_length < len(file_content):
                    snippet += "..."
                
                content_data["text_matches"] = snippet
            except Exception:
                # Ignore content retrieval errors for search results
                content_data["text_matches"] = "[Content unavailable]"
            
            results_list.append(content_data)
            count += 1
        
        return _success_response({
            "items": results_list,
            "count": len(results_list),
            "query": query_builder
        })
        
    except Exception as e:
        return _error_response(f"Unexpected error: {str(e)}")
