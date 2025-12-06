import pandas as pd
import jinja2
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import io

class ReportGenerator:
    def generate_csv(self, test_results: list) -> str:
        """
        Generates CSV report
        """
        df = pd.DataFrame(test_results)
        return df.to_csv(index=False)

    def generate_html(self, test_results: list, ai_analysis: list) -> str:
        """
        Generates HTML report
        """
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Accessibility Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 2em; }
                .header { background: #f0f0f0; padding: 1em; }
                .issue { border: 1px solid #ddd; margin: 1em 0; padding: 1em; }
                .fail { color: #dc3545; }
                .pass { color: #28a745; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Accessibility Test Report</h1>
                <p>Total Tests: {{ test_results|length }}</p>
            </div>
            
            <h2>Test Results</h2>
            {% for result in test_results %}
            <div class="issue">
                <h3 class="{{ result.status }}">{{ result.status|upper }}: {{ result.description }}</h3>
                <p><strong>Rule:</strong> {{ result.rule }}</p>
                <p><strong>Location:</strong> {{ result.location }}</p>
                {% if result.status == 'fail' %}
                <p><strong>Impact:</strong> {{ result.impact }}</p>
                {% endif %}
            </div>
            {% endfor %}

            <h2>AI Analysis</h2>
            {% for analysis in ai_analysis %}
            <div class="issue">
                <h3>{{ analysis.title }}</h3>
                <p><strong>Location:</strong> {{ analysis.location }}</p>
                <p><strong>Problem:</strong> {{ analysis.problem }}</p>
                <p><strong>Recommendation:</strong> {{ analysis.recommendation }}</p>
            </div>
            {% endfor %}
        </body>
        </html>
        """
        
        env = jinja2.Environment()
        template = env.from_string(template)
        return template.render(test_results=test_results, ai_analysis=ai_analysis)

    def generate_pdf(self, test_results: list, ai_analysis: list) -> bytes:
        """
        Generates PDF report
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        elements.append(Paragraph("Accessibility Test Report", styles['Title']))
        elements.append(Spacer(1, 12))

        # Summary
        total_tests = len(test_results)
        passed_tests = sum(1 for test in test_results if test['status'] == 'pass')
        failed_tests = total_tests - passed_tests

        summary_data = [
            ['Total Tests', str(total_tests)],
            ['Passed Tests', str(passed_tests)],
            ['Failed Tests', str(failed_tests)]
        ]

        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
