"""
Setup configuration for the Coding Assistant.
"""

from setuptools import setup, find_packages

setup(
    name="coding_assistant",
    version="0.1.0",
    description="An intelligent coding assistant built with Google's Agent Development Kit",
    author="",
    author_email="",
    packages=find_packages(),
    install_requires=[
        "google-adk>=0.2.0",
        "google-generativeai>=0.3.0",
    ],
    python_requires=">=3.9",
)
