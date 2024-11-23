import pandas as pd
import os


class QodoService:
    def __init__(self, spreadsheet_path: str):
        self.spreadsheet_path = spreadsheet_path
        self.prompts = self._load_prompts()

    def _load_prompts(self):
        """Load prompts, expected code, and test cases from a spreadsheet."""
        if not os.path.exists(self.spreadsheet_path):
            raise FileNotFoundError(f"Spreadsheet not found: {self.spreadsheet_path}")

        try:
            df = pd.read_excel(self.spreadsheet_path)
        except Exception as e:
            raise ValueError(f"Failed to load spreadsheet: {e}")

        if not {"Prompt", "Expected Code", "Test Case"}.issubset(df.columns):
            raise ValueError("Spreadsheet must contain 'Prompt', 'Expected Code', and 'Test Case' columns.")

        return df.to_dict("records")

    def generate_suggestion(self, prompt: str) -> str:
        """
        Simulate Copilot's response.
        Replace this with actual Copilot suggestions if available.
        """
        mock_responses = {
            "Write a function to calculate the factorial of a number.": """
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
""",
            "Write a function to reverse a string.": """
def reverse_string(s):
    return s[::-1]
"""
        }
        return mock_responses.get(prompt, "# No suggestion available")

    def execute_code(self, code: str, test_case: str):
        """
        Dynamically execute code and test case.
        """
        local_scope = {}
        try:
            exec(code, {}, local_scope)
            exec(test_case, {}, local_scope)
            return True, "Test passed."
        except Exception as e:
            return False, str(e)

    def run_tests(self):
        """
        Run tests for all prompts from the spreadsheet and update the spreadsheet with results.
        """
        results = []
        for index, prompt_data in enumerate(self.prompts):
            prompt = prompt_data["Prompt"]
            expected_code = prompt_data["Expected Code"]
            test_case = prompt_data["Test Case"]

            # Generate suggestion
            suggestion = self.generate_suggestion(prompt)

            # Compare generated suggestion with expected code
            if suggestion.strip() != expected_code.strip():
                results.append({
                    "index": index,
                    "status": "fail",
                    "error": "Generated code does not match expected output."
                })
                continue

            # Execute and test suggestion
            passed, message = self.execute_code(suggestion, test_case)
            results.append({
                "index": index,
                "status": "pass" if passed else "fail",
                "error": None if passed else message
            })

        # Update the spreadsheet with test results
        self._update_spreadsheet(results)
        return results

    def _update_spreadsheet(self, results):
        """Update the spreadsheet with the test results."""
        df = pd.read_excel(self.spreadsheet_path)

        # Update the 'Test Status' column with results
        for result in results:
            df.loc[result["index"], "Test Status"] = result["status"]
            if result["error"]:
                df.loc[result["index"], "Error Message"] = result["error"]

        # Write the updated data back to the spreadsheet
        df.to_excel(self.spreadsheet_path, index=False)

        print("Spreadsheet updated with test results.")


if __name__ == "__main__":
    # Define the spreadsheet path
    spreadsheet_path = "prompts.xlsx"

    # Initialize the service and run tests
    service = QodoService(spreadsheet_path)
    test_results = service.run_tests()

    # Print results
    for result in test_results:
        print(f"Prompt: {result['status']}")
        if result.get('error'):
            print(f"Error: {result['error']}")
        print("-" * 40)