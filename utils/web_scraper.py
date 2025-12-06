from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class WebScraper:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-software-rasterizer')

    def scrape(self, url: str) -> str:
        """
        Scrapes a webpage including dynamic content using Selenium
        """
        driver = None
        try:
            # Initialize WebDriver with default service
            service = Service()
            driver = webdriver.Chrome(service=service, options=self.options)

            # Set page load timeout
            driver.set_page_load_timeout(30)

            # Load the page
            print(f"Attempting to load URL: {url}")
            driver.get(url)

            # Wait for dynamic content to load
            try:
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script('return document.readyState') == 'complete'
                )
                print("Page load complete")
            except Exception as wait_error:
                print(f"Warning: Timeout waiting for page load: {str(wait_error)}")
                # Continue with partial content

            # Get the page source after JavaScript execution
            html_content = driver.page_source
            print("Successfully retrieved page source")

            return html_content

        except Exception as e:
            print(f"Error during web scraping: {str(e)}")
            raise Exception(f"Failed to scrape webpage: {str(e)}")
        finally:
            if driver:
                driver.quit()
                print("WebDriver closed")