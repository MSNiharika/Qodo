import pytest
from qodo_service import QodoService

@pytest.fixture
def copilot_service():
    return QodoService(spreadsheet_path="prompts.xlsx")

def test_prompts_loading(copilot_service):
    assert len(copilot_service.prompts) > 0, "No prompts loaded from spreadsheet."

def test_generate_suggestion(copilot_service):
    suggestion = copilot_service.generate_suggestion("Write a function to calculate the factorial of a number.")
    assert "def factorial(n)" in suggestion, "Suggestion does not match expected output."

def test_run_tests(copilot_service):
    results = copilot_service.run_tests()
    for result in results:
        assert result["status"] == "pass", f"Test failed: {result['error']}"