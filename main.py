import streamlit as st
import pandas as pd
from utils.web_scraper import WebScraper
from utils.accessibility_tester import AccessibilityTester
from utils.ai_analyzer import AIAnalyzer
from utils.report_generator import ReportGenerator
import plotly.express as px
import base64
from pathlib import Path
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Web Accessibility Tester",
    page_icon="🌐",
    layout="wide"
)

# Load custom CSS
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

def main():
    st.title("🌐 Web Accessibility Testing Tool")
    st.markdown("### Powered by AI & WCAG 2.2 Standards")

    # URL Input
    url = st.text_input("Enter website URL to test:", placeholder="https://example.com")
    
    # WCAG Version Selection
    wcag_version = st.selectbox(
        "Select WCAG Version",
        ["WCAG 2.2", "WCAG 2.1", "WCAG 2.0"],
        index=0
    )

    if st.button("Run Accessibility Test", type="primary"):
        if url:
            try:
                with st.spinner("🔍 Analyzing webpage..."):
                    # Initialize components
                    scraper = WebScraper()
                    tester = AccessibilityTester()
                    analyzer = AIAnalyzer()
                    report_gen = ReportGenerator()

                    # Scrape webpage
                    html_content = scraper.scrape(url)
                    
                    # Run accessibility tests
                    test_results = tester.run_tests(html_content, wcag_version)
                    
                    # AI Analysis
                    ai_analysis = analyzer.analyze_issues(test_results)
                    
                    # Display Results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📊 Test Summary")
                        total_tests = len(test_results)
                        passed_tests = sum(1 for test in test_results if test['status'] == 'pass')
                        failed_tests = total_tests - passed_tests
                        
                        # Create summary chart
                        summary_df = pd.DataFrame({
                            'Status': ['Passed', 'Failed'],
                            'Count': [passed_tests, failed_tests]
                        })
                        fig = px.pie(summary_df, values='Count', names='Status',
                                   color_discrete_sequence=['#00CC96', '#EF553B'])
                        st.plotly_chart(fig)

                    with col2:
                        st.subheader("🎯 Impact Distribution")
                        impact_counts = pd.DataFrame(
                            [result['impact'] for result in test_results if 'impact' in result]
                        ).value_counts().reset_index()
                        impact_counts.columns = ['Impact', 'Count']
                        fig = px.bar(impact_counts, x='Impact', y='Count',
                                   color='Impact',
                                   color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96'])
                        st.plotly_chart(fig)

                    # Display Issues Table
                    st.subheader("📋 Detailed Issues")
                    issues_df = pd.DataFrame(test_results)
                    st.dataframe(issues_df)

                    # AI Recommendations
                    st.subheader("🤖 AI Analysis & Recommendations")
                    for issue in ai_analysis:
                        with st.expander(f"Issue: {issue['title']}"):
                            st.markdown(f"**Location:** {issue['location']}")
                            st.markdown(f"**Problem:** {issue['problem']}")
                            st.markdown(f"**Recommendation:** {issue['recommendation']}")

                    # Export Options
                    st.subheader("📥 Export Results")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        csv = report_gen.generate_csv(test_results)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="accessibility_report.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        html_report = report_gen.generate_html(test_results, ai_analysis)
                        st.download_button(
                            label="Download HTML Report",
                            data=html_report,
                            file_name="accessibility_report.html",
                            mime="text/html"
                        )
                    
                    with col3:
                        pdf_report = report_gen.generate_pdf(test_results, ai_analysis)
                        st.download_button(
                            label="Download PDF Report",
                            data=pdf_report,
                            file_name="accessibility_report.pdf",
                            mime="application/pdf"
                        )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a URL to test")

if __name__ == "__main__":
    main()
