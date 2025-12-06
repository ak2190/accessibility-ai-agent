# Web Accessibility Testing Tool 🌐

A sophisticated Streamlit-based web accessibility testing application powered by AI and advanced web scraping technologies. This tool performs comprehensive accessibility analysis against WCAG standards, leveraging machine learning insights and automated testing frameworks.

## Features ✨

- **Automated Accessibility Testing**: Scans websites for WCAG 2.0, 2.1, and 2.2 compliance
- **AI-Powered Analysis**: Utilizes OpenAI GPT-4o for intelligent issue analysis and recommendations
- **Interactive Dashboard**: Real-time visualization of accessibility test results
- **Comprehensive Reports**: Generate detailed reports in multiple formats (CSV, HTML, PDF)
- **Data Visualization**: Interactive charts and graphs showing test results and impact distribution
- **Multi-Standard Support**: Test against different WCAG versions
- **Detailed Recommendations**: AI-generated suggestions for fixing accessibility issues

## Prerequisites 🛠️

Before running the application, ensure you have the following installed:
- Python 3.11 or higher
- Google Chrome browser
- ChromeDriver (matching your Chrome version)

## Installation Guide 📥

1. **Clone the Repository**
   ```bash
   git clone [repository-url]
   cd web-accessibility-tester
   ```

2. **Install Python Dependencies**
   ```bash
   pip install streamlit pandas openai plotly reportlab selenium axe-selenium-python python-dotenv trafilatura
   ```

3. **ChromeDriver Setup**
   - Download ChromeDriver from [https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/)
   - Make sure the ChromeDriver version matches your Chrome browser version
   - Add ChromeDriver to your system PATH

4. **Environment Configuration**
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Running the Application 🚀

1. Navigate to the project directory
   ```bash
   cd web-accessibility-tester
   ```

2. Start the Streamlit application
   ```bash
   streamlit run main.py
   ```

3. Open your browser and go to:
   ```
   http://localhost:5000
   ```

## Usage Guide 📖

1. Enter the URL of the website you want to test in the input field
2. Select the WCAG version for testing (2.0, 2.1, or 2.2)
3. Click "Run Accessibility Test"
4. View the results in the interactive dashboard:
   - Test Summary
   - Impact Distribution
   - Detailed Issues List
   - AI-Generated Recommendations
5. Export results in your preferred format (CSV, HTML, or PDF)

## Project Structure 📁

```
├── .streamlit/          # Streamlit configuration
├── assets/             # Static assets and styles
├── utils/              # Utility modules
│   ├── web_scraper.py          # Web scraping functionality
│   ├── accessibility_tester.py  # Accessibility testing logic
│   ├── ai_analyzer.py          # AI analysis integration
│   └── report_generator.py     # Report generation utilities
├── main.py            # Main application file
└── .env              # Environment variables
```

## Troubleshooting 🔧

1. **ChromeDriver Issues**
   - Ensure ChromeDriver version matches your Chrome browser version
   - Verify ChromeDriver is in your system PATH
   - Try running Chrome in headless mode if you encounter display issues

2. **OpenAI API Issues**
   - Verify your API key is correctly set in the .env file
   - Check your API usage limits and billing status

3. **Streamlit Port Issues**
   - If port 5000 is in use, modify the port in `.streamlit/config.toml`

## Known Limitations ⚠️

- The tool requires an active internet connection
- Some dynamic content may not be captured in single-page applications
- API rate limits may apply for the AI analysis feature
- Large websites may take longer to analyze

## Support and Feedback 💬

For issues, questions, or feedback, please open an issue in the repository or contact the development team.
