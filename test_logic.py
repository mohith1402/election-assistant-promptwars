import pytest
from app import SYSTEM_INSTRUCTION

def test_system_prompt_safety_rules():
    """Validates that the core non-partisan rules are present in the AI instructions."""
    instruction_lower = SYSTEM_INSTRUCTION.lower()
    
    assert "non-partisan" in instruction_lower, "AI must be instructed to remain non-partisan."
    assert "bias" in instruction_lower, "AI must be explicitly told to avoid political bias."
    assert "simple" in instruction_lower, "AI must be instructed to use simple language."
    
def test_app_architecture():
    """Validates the application has the correct configuration files for deployment."""
    import os
    assert os.path.exists("Dockerfile"), "Dockerfile is missing for Cloud Run deployment."
    assert os.path.exists("requirements.txt"), "Requirements file is missing."
