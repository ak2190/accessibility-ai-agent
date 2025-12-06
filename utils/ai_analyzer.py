import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        self.model = "gpt-4o"

    def analyze_issues(self, test_results: list) -> list:
        """
        Analyzes accessibility issues using OpenAI
        """
        try:
            # Filter failed tests
            failed_tests = [test for test in test_results if test['status'] == 'fail']

            analyzed_issues = []

            for issue in failed_tests:
                prompt = f"""
                Analyze this web accessibility issue and provide recommendations:
                Rule: {issue['rule']}
                Description: {issue['description']}
                Element: {issue['element']}
                Impact: {issue['impact']}

                Provide a response in the following JSON format:
                {{
                    "problem": "Clear explanation of the issue",
                    "recommendation": "Specific steps to fix the issue",
                    "impact_analysis": "Description of accessibility impact"
                }}
                """

                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        response_format={"type": "json_object"}
                    )

                    # Extract the content from the response
                    analysis_text = response.choices[0].message.content

                    # Parse the JSON content
                    import json
                    analysis = json.loads(analysis_text)

                    analyzed_issues.append({
                        "title": issue.get('description', 'Unknown Issue'),
                        "location": issue.get('location', 'Not specified'),
                        "problem": analysis.get('problem', 'No problem description available'),
                        "recommendation": analysis.get('recommendation', 'No recommendation available'),
                        "impact": issue.get('impact', 'Unknown')
                    })

                except json.JSONDecodeError as json_err:
                    print(f"Error parsing AI response: {json_err}")
                    # Add a fallback analysis if JSON parsing fails
                    analyzed_issues.append({
                        "title": issue.get('description', 'Unknown Issue'),
                        "location": issue.get('location', 'Not specified'),
                        "problem": "Error analyzing issue",
                        "recommendation": "Please try again or contact support",
                        "impact": issue.get('impact', 'Unknown')
                    })
                except Exception as e:
                    print(f"Error during AI analysis: {str(e)}")
                    continue

            return analyzed_issues

        except Exception as e:
            raise Exception(f"Failed to analyze issues: {str(e)}")