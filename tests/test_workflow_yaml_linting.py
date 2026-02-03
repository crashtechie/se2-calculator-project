"""
Tests for GitHub Actions workflow YAML formatting.

Feature: fix-workflow-yaml-linting
"""

import re
from pathlib import Path

import pytest
import yaml


WORKFLOW_FILE = Path(__file__).parent.parent / ".github/workflows/test.yml"


@pytest.fixture
def workflow_content():
    """Load the workflow file content."""
    return WORKFLOW_FILE.read_text()


@pytest.fixture
def workflow_data(workflow_content):
    """Parse the workflow YAML."""
    return yaml.safe_load(workflow_content)



def test_document_starts_with_marker(workflow_content):
    """
    Verify file begins with YAML document start marker.
    
    **Validates: Requirements 1.1**
    """
    assert workflow_content.startswith("---\n"), "File must start with '---' followed by newline"



def test_file_ends_with_newline(workflow_content):
    """
    Verify file ends with exactly one newline character.
    
    **Validates: Requirements 4.1**
    """
    assert workflow_content.endswith("\n"), "File must end with a newline character"
    assert not workflow_content.endswith("\n\n"), "File must end with exactly one newline"



def test_yaml_structure_preservation(workflow_data):
    """
    Property 1: YAML Structure Preservation
    
    Verify that the parsed YAML structure contains all expected keys and values.
    This ensures formatting changes don't alter the semantic meaning.
    
    **Validates: Requirements 5.2**
    Tag: Feature: fix-workflow-yaml-linting, Property 1: YAML structure preservation
    """
    # Verify top-level structure
    assert "name" in workflow_data
    assert workflow_data["name"] == "Tests"
    
    # Note: YAML parsers convert "on" to boolean True, which is expected behavior
    # GitHub Actions accepts both "on" and True as valid
    assert True in workflow_data or "on" in workflow_data
    on_key = True if True in workflow_data else "on"
    
    assert "push" in workflow_data[on_key]
    assert "pull_request" in workflow_data[on_key]
    
    # Verify branch configurations
    push_branches = workflow_data[on_key]["push"]["branches"]
    assert "main" in push_branches
    assert "development" in push_branches
    assert "enhancement/**" in push_branches
    
    pr_branches = workflow_data[on_key]["pull_request"]["branches"]
    assert "main" in pr_branches
    assert "development" in pr_branches
    
    # Verify jobs structure
    assert "jobs" in workflow_data
    assert "test" in workflow_data["jobs"]
    assert workflow_data["jobs"]["test"]["runs-on"] == "ubuntu-latest"
    
    # Verify steps exist
    steps = workflow_data["jobs"]["test"]["steps"]
    assert len(steps) == 6
    
    step_names = [step["name"] for step in steps]
    assert "Checkout code" in step_names
    assert "Setup Python 3.13" in step_names
    assert "Install UV" in step_names
    assert "Install dependencies" in step_names
    assert "Run tests with coverage" in step_names
    assert "Upload coverage to Codecov" in step_names



def test_no_trailing_whitespace(workflow_content):
    """
    Property 2: No Trailing Whitespace
    
    Verify that no line in the file ends with whitespace characters.
    
    **Validates: Requirements 3.1**
    Tag: Feature: fix-workflow-yaml-linting, Property 2: No trailing whitespace
    """
    lines = workflow_content.split("\n")
    
    for line_num, line in enumerate(lines, start=1):
        # Skip the last empty line (after final newline)
        if line_num == len(lines) and line == "":
            continue
            
        assert not line.endswith(" "), f"Line {line_num} has trailing spaces"
        assert not line.endswith("\t"), f"Line {line_num} has trailing tabs"



def test_correct_bracket_spacing(workflow_content):
    """
    Property 3: Correct Bracket Spacing
    
    Verify that bracket-enclosed arrays have no extra spaces inside brackets.
    
    **Validates: Requirements 2.1, 2.2**
    Tag: Feature: fix-workflow-yaml-linting, Property 3: Correct bracket spacing
    """
    # Find all bracket-enclosed arrays
    bracket_pattern = re.compile(r'\[([^\]]+)\]')
    matches = bracket_pattern.findall(workflow_content)
    
    for match in matches:
        # Check no leading/trailing spaces inside brackets
        assert not match.startswith(" "), f"Array [{match}] has leading space"
        assert not match.endswith(" "), f"Array [{match}] has trailing space"
        
        # Check no multiple consecutive spaces
        assert "  " not in match, f"Array [{match}] has multiple consecutive spaces"
