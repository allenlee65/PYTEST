import pytest
import time
import os
import smtplib
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import random
import string

class TestResultCollector:
    """Collects test results for email reporting"""
    test_results = {
        'passed': [],
        'failed': [],
        'skipped': [],
        'total_tests': 0,
        'execution_time': '',
        'start_time': None,
        'end_time': None
    }

    @classmethod
    def reset_results(cls):
        """Reset test results"""
        cls.test_results = {
            'passed': [],
            'failed': [],
            'skipped': [],
            'total_tests': 0,
            'execution_time': '',
            'start_time': datetime.now(),
            'end_time': None
        }

    @classmethod
    def add_result(cls, test_name, status, error_msg=None):
        """Add test result"""
        cls.test_results['total_tests'] += 1
        
        if status == 'PASSED':
            cls.test_results['passed'].append(test_name)
        elif status == 'FAILED':
            cls.test_results['failed'].append({
                'name': test_name,
                'error': error_msg or 'Unknown error'
            })
        elif status == 'SKIPPED':
            cls.test_results['skipped'].append(test_name)

    @classmethod
    def send_test_report_email(cls):
        """Send test execution report via email"""
        try:
            # Set end time
            cls.test_results['end_time'] = datetime.now()
            
            # Email configuration
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = os.getenv('SENDER_EMAIL', 'your_email@gmail.com')
            sender_password = os.getenv('EMAIL_PASSWORD', 'your_app_password')
            recipient_email = "allenlee0611@gmail.com"
            
            # Calculate execution time
            if cls.test_results['end_time'] and cls.test_results['start_time']:
                execution_time = cls.test_results['end_time'] - cls.test_results['start_time']
                cls.test_results['execution_time'] = str(execution_time)
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"Automation Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Create HTML email body
            html_body = cls.create_html_report()
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            
            print(f"Test report sent successfully to {recipient_email}")
            
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
    
    @classmethod
    def create_html_report(cls):
        """Create HTML formatted test report"""
        total_tests = cls.test_results['total_tests']
        passed_count = len(cls.test_results['passed'])
        failed_count = len(cls.test_results['failed'])
        skipped_count = len(cls.test_results['skipped'])
        success_rate = (passed_count / total_tests * 100) if total_tests > 0 else 0
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 10px; text-align: center; }}
                .summary {{ background-color: #f2f2f2; padding: 15px; margin: 10px 0; }}
                .passed {{ color: #4CAF50; }}
                .failed {{ color: #f44336; }}
                .skipped {{ color: #ff9800; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .status-passed {{ background-color: #d4edda; }}
                .status-failed {{ background-color: #f8d7da; }}
                .status-skipped {{ background-color: #fff3cd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Docker Automation Test Report</h1>
                <p>Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Environment: Docker Container</p>
            </div>
            
            <div class="summary">
                <h2>Test Summary</h2>
                <p><strong>Total Tests:</strong> {total_tests}</p>
                <p><strong class="passed">Passed:</strong> {passed_count}</p>
                <p><strong class="failed">Failed:</strong> {failed_count}</p>
                <p><strong class="skipped">Skipped:</strong> {skipped_count}</p>
                <p><strong>Success Rate:</strong> {success_rate:.1f}%</p>
                <p><strong>Execution Time:</strong> {cls.test_results['execution_time']}</p>
            </div>
            
            <h2>Test Details</h2>
            <table>
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Details</th>
                </tr>
        """
        
        # Add passed tests
        for test in cls.test_results['passed']:
            html += f"""
                <tr class="status-passed">
                    <td>{test}</td>
                    <td class="passed">PASSED</td>
                    <td>Test executed successfully</td>
                </tr>
            """
        
        # Add failed tests
        for test_info in cls.test_results['failed']:
            test_name = test_info.get('name', 'Unknown')
            error_msg = test_info.get('error', 'No error message')
            if len(error_msg) > 200:
                error_msg = error_msg[:200] + "..."
            html += f"""
                <tr class="status-failed">
                    <td>{test_name}</td>
                    <td class="failed">FAILED</td>
                    <td>{error_msg}</td>
                </tr>
            """
        
        # Add skipped tests
        for test in cls.test_results['skipped']:
            html += f"""
                <tr class="status-skipped">
                    <td>{test}</td>
                    <td class="skipped">SKIPPED</td>
                    <td>Test was skipped</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        return html

@pytest.mark.flaky(reruns=3, reruns_delay=2)
class TestAutomationExercise:
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method to initialize WebDriver before each test"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.geolocation": 2
        })
        
        # Use the system chromedriver
        service = Service('/usr/local/bin/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://automationexercise.com"
        self.DOWNLOAD_DIR = "/app/downloads"
        
        yield
        # Teardown
        self.driver.quit()

    def generate_random_email(self):
        """Generate random email for testing"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_string}@example.com"

    def generate_random_name(self):
        """Generate random name for testing"""
        names = ["John", "Jane", "Mike", "Sarah", "David", "Emma", "Alex", "Lisa"]
        return random.choice(names) + str(random.randint(100, 999))

    # Your existing test methods...
    # Add try-catch blocks to all test methods for result collection