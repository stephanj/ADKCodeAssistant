"""
Common data schema and types for coding-assistant agents.
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from google.genai import types

# Convenient declaration for controlled generation
json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)

class FileInfo(BaseModel):
    """Information about a file."""
    name: str = Field(description="Name of the file")
    path: str = Field(description="Full path to the file")
    size: Optional[int] = Field(description="Size of the file in bytes")
    type: str = Field(description="Type of the file, e.g., 'python', 'javascript', etc.")
    last_modified: Optional[str] = Field(description="Last modified date of the file")

class DirectoryInfo(BaseModel):
    """Information about a directory."""
    name: str = Field(description="Name of the directory")
    path: str = Field(description="Full path to the directory")
    files: List[FileInfo] = Field(description="Files in the directory")
    directories: List["DirectoryInfo"] = Field(description="Subdirectories in the directory")

class ProjectStructure(BaseModel):
    """Structure of a project."""
    root: str = Field(description="Root directory of the project")
    structure: DirectoryInfo = Field(description="Structure of the project")

class CodeAnalysis(BaseModel):
    """Analysis of code."""
    file_path: str = Field(description="Path to the file being analyzed")
    language: str = Field(description="Programming language of the code")
    imports: List[str] = Field(description="List of imports in the code")
    functions: List[Dict[str, Any]] = Field(description="List of functions in the code")
    classes: List[Dict[str, Any]] = Field(description="List of classes in the code")
    complexity: Dict[str, Any] = Field(description="Complexity analysis of the code")
    issues: List[Dict[str, Any]] = Field(description="List of issues found in the code")

class PlanTask(BaseModel):
    """A task in a plan."""
    id: str = Field(description="Unique identifier for the task")
    title: str = Field(description="Title of the task")
    description: str = Field(description="Description of the task")
    priority: str = Field(description="Priority of the task (high, medium, low)")
    estimated_effort: str = Field(description="Estimated effort for the task")
    dependencies: List[str] = Field(description="List of task IDs that this task depends on")

class ImplementationPlan(BaseModel):
    """A plan for implementing a feature or component."""
    feature: str = Field(description="Name of the feature or component")
    description: str = Field(description="Description of the feature or component")
    tasks: List[PlanTask] = Field(description="List of tasks for implementing the feature")

class GeneratedCode(BaseModel):
    """Generated code."""
    file_path: str = Field(description="Path to the file being generated")
    language: str = Field(description="Programming language of the code")
    code: str = Field(description="The generated code")
    description: str = Field(description="Description of the generated code")
    tests: Optional[str] = Field(description="Tests for the generated code")

class ReviewComment(BaseModel):
    """A review comment on code."""
    file_path: str = Field(description="Path to the file being reviewed")
    line_number: Optional[int] = Field(description="Line number of the comment")
    severity: str = Field(description="Severity of the issue (critical, major, minor, info)")
    issue_type: str = Field(description="Type of issue (bug, performance, security, style, etc.)")
    description: str = Field(description="Description of the issue")
    suggestion: Optional[str] = Field(description="Suggestion for fixing the issue")

class CodeReview(BaseModel):
    """A code review."""
    file_path: str = Field(description="Path to the file being reviewed")
    language: str = Field(description="Programming language of the code")
    overall_quality: str = Field(description="Overall quality assessment of the code")
    comments: List[ReviewComment] = Field(description="List of review comments")
    positive_aspects: List[str] = Field(description="List of positive aspects of the code")
    areas_for_improvement: List[str] = Field(description="List of areas for improvement")
