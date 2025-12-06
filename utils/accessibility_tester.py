from axe_selenium_python import Axe
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

class AccessibilityTester:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

    def run_tests(self, html_content: str, wcag_version: str) -> list:
        """
        Runs accessibility tests using axe-core
        """
        try:
            driver = webdriver.Chrome(options=self.options)

            # Create a temporary HTML file with the content
            temp_path = os.path.abspath('temp.html')
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Load the temporary file with file:// protocol
            driver.get(f'file://{temp_path}')

            # Initialize axe with proper injection
            axe = Axe(driver)
            axe.inject()  # This is crucial - inject the axe-core javascript

            # Run axe analysis
            results = axe.run()

            # Process results
            processed_results = []

            # Process violations
            for violation in results["violations"]:
                for node in violation["nodes"]:
                    processed_results.append({
                        "status": "fail",
                        "impact": violation["impact"],
                        "rule": violation["id"],
                        "description": violation["description"],
                        "element": node["html"],
                        "location": node["target"][0],
                        "help": violation["help"]
                    })

            # Process passes
            for pass_result in results["passes"]:
                for node in pass_result["nodes"]:
                    processed_results.append({
                        "status": "pass",
                        "rule": pass_result["id"],
                        "description": pass_result["description"],
                        "element": node["html"],
                        "location": node["target"][0]
                    })

            return processed_results

        except Exception as e:
            if 'driver' in locals():
                driver.quit()
            raise Exception(f"Failed to run accessibility tests: {str(e)}")
        finally:
            if 'driver' in locals():
                driver.quit()
            # Clean up temporary file
            if os.path.exists('temp.html'):
                try:
                    os.remove('temp.html')
                except:
                    pass