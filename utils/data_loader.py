import json

def load_test_data(filepath):
    with open(filepath, "r") as f:
        return json.load(f)