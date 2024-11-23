import requests
from utils.data_loader import load_test_data
import pytest

config = load_test_data("config/config.json")
test_data = load_test_data("config/test_data.json")["valid_inputs"]

# This part of the test make an pi call to Qodo service
# This would be supported only if Qodo is able to expose the apis based json results for prompts
@pytest.mark.parametrize("case", test_data)
def test_functionality(case):
    response = requests.post(config["api_endpoint"], json={"input": case["input"]}, timeout=config["timeout"])
    assert response.status_code == 200
    assert response.json()["response"] == case["expected_output"]