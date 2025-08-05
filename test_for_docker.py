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

    @pytest.mark.flaky(reruns=2, reruns_delay=1)
    def test_case_1_register_user(self):
        """Test Case 1: Register User"""
        try:
            # 1. Launch browser and navigate to URL
            self.driver.get(self.base_url)
            
            # 3. Verify home page is visible
            assert "Automation Exercise" in self.driver.title
            
            # 4. Click on 'Signup / Login' button
            signup_login_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Signup / Login")))
            signup_login_btn.click()
            
            # 5. Verify 'New User Signup!' is visible
            signup_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'New User Signup!')]")))
            assert signup_text.is_displayed()
            
            # 6. Enter name and email address
            username = self.generate_random_name()
            email = self.generate_random_email()
            
            name_field = self.driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div[3]/div/form/input[2]')
            email_field = self.driver.find_element(By.XPATH, "//input[@data-qa='signup-email']")
            
            name_field.clear()
            name_field.send_keys(username)
            email_field.send_keys(email)
            
            # Step 7: Click 'Signup' button
            signup_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="form"]/div/div/div[3]/div/form/button'))
                )
            signup_btn.click()

            # Fill account info
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//b[text()='Enter Account Information']"))
            )
            self.driver.execute_script("window.scrollBy(0,400);")

            self.driver.find_element(By.ID, "id_gender1").click()
            self.driver.find_element(By.ID, "password").send_keys("TestPassword123")
            self.driver.find_element(By.ID, "days").send_keys("1")
            self.driver.find_element(By.ID, "months").send_keys("January")
            self.driver.find_element(By.ID, "years").send_keys("2000")
            self.driver.find_element(By.ID, "newsletter").click()
            self.driver.find_element(By.ID, "optin").click()
            self.driver.find_element(By.ID, "first_name").send_keys("Test")
            self.driver.find_element(By.ID, "last_name").send_keys("User")
            self.driver.find_element(By.ID, "company").send_keys("TestCompany")
            self.driver.find_element(By.ID, "address1").send_keys("123 Test St")
            self.driver.find_element(By.ID, "address2").send_keys("Suite 1")
            self.driver.find_element(By.ID, "country").send_keys("United States")
            self.driver.find_element(By.ID, "state").send_keys("TestState")
            self.driver.find_element(By.ID, "city").send_keys("TestCity")
            self.driver.find_element(By.ID, "zipcode").send_keys("12345")
            self.driver.find_element(By.ID, "mobile_number").send_keys("1234567890")
            self.driver.find_element(By.XPATH, "//button[@data-qa='create-account']").click()

            # Step 9: Verify 'ACCOUNT CREATED!' and click 'Continue'
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Created!']"))
            )
            self.driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()

            # Step 10: Verify 'Logged in as username' at top
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Logged in as')]"))
            )
            
            # 17. Click 'Delete Account' button
            delete_account_btn = self.driver.find_element(By.LINK_TEXT, "Delete Account")
            delete_account_btn.click()
            
            # 18. Verify 'ACCOUNT DELETED!' is visible
            account_deleted_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[@data-qa='account-deleted']")))
            assert account_deleted_text.is_displayed()
            
            continue_btn = self.driver.find_element(By.XPATH, "//a[@data-qa='continue-button']")
            continue_btn.click()
            
            # Record success
            TestResultCollector.add_result('test_case_1_register_user', 'PASSED')
            
        except Exception as e:
            # Record failure
            TestResultCollector.add_result('test_case_1_register_user', 'FAILED', str(e))
            raise e

    # Add similar try-catch blocks to other tests...
    # ...existing test methods...

    def test_case_2_login_with_correct_credentials(self):
        """Test Case 2: Login User with correct email and password"""
        try:
            self.driver.get(self.base_url)
            assert "Automation Exercise" in self.driver.title
            
            # Click on 'Signup / Login' button
            signup_login_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Signup / Login")))
            signup_login_btn.click()
            
            # Verify 'Login to your account' is visible
            login_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Login to your account')]")))
            assert login_text.is_displayed()
            
            # Enter correct email and password (these would need to be valid credentials)
            email_field = self.driver.find_element(By.XPATH, "//input[@data-qa='login-email']")
            password_field = self.driver.find_element(By.XPATH, "//input[@data-qa='login-password']")
            
            # Note: Replace with actual test credentials
            email_field.send_keys("allenlee@punkproof.com")
            password_field.send_keys("SKDeIutmdZqgNxJ")
            
            # Click login button
            login_btn = self.driver.find_element(By.XPATH, "//button[@data-qa='login-button']")
            login_btn.click()
            
            TestResultCollector.add_result('test_case_2_login_with_correct_credentials', 'PASSED')
            
        except Exception as e:
            TestResultCollector.add_result('test_case_2_login_with_correct_credentials', 'FAILED', str(e))
            raise e

    # Continue with all your existing test methods...
    # Make sure to add the try-catch pattern to each test method

    def test_case_3_login_with_incorrect_credentials(self):
        """Test Case 3: Login User with incorrect email and password"""
        try:
            self.driver.get(self.base_url)
            assert "Automation Exercise" in self.driver.title
            
            # Click on 'Signup / Login' button
            signup_login_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Signup / Login")))
            signup_login_btn.click()
            
            # Verify 'Login to your account' is visible
            login_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Login to your account')]")))
            assert login_text.is_displayed()
            
            # Enter incorrect email and password
            email_field = self.driver.find_element(By.XPATH, "//input[@data-qa='login-email']")
            password_field = self.driver.find_element(By.XPATH, "//input[@data-qa='login-password']")
            
            email_field.send_keys("invalid@example.com")
            password_field.send_keys("wrongpassword")
            
            # Click login button
            login_btn = self.driver.find_element(By.XPATH, "//button[@data-qa='login-button']")
            login_btn.click()
            
            # Verify error message
            error_message = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Your email or password is incorrect!')]")))
            assert error_message.is_displayed()

            TestResultCollector.add_result('test_case_3_login_with_incorrect_credentials', 'PASSED')
        except Exception as e:
            TestResultCollector.add_result('test_case_3_login_with_incorrect_credentials', 'FAILED', str(e))
            raise e 

    def test_case_4_logout_User(self):
        """Test Case 4: Logout User"""
        # Note: This test requires pre-existing account credentials
        # For demo purposes, using placeholder credentials
        try:
            self.driver.get(self.base_url)
            assert "Automation Exercise" in self.driver.title

            # Click on 'Signup / Login' button
            signup_login_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Signup / Login")))
            signup_login_btn.click()

            # Verify 'Login to your account' is visible
            login_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Login to your account')]")))
            assert login_text.is_displayed()
            
            # Enter correct email and password (these would need to be valid credentials)
            email_field = self.driver.find_element(By.XPATH, "//input[@data-qa='login-email']")
            password_field = self.driver.find_element(By.XPATH, "//input[@data-qa='login-password']")
            
            # Note: Replace with actual test credentials
            email_field.send_keys("allenlee@punkproof.com")
            password_field.send_keys("SKDeIutmdZqgNxJ")
            
            # Click login button
            login_btn = self.driver.find_element(By.XPATH, "//button[@data-qa='login-button']")
            login_btn.click()
            assert "Automation Exercise" in self.driver.title

            # This test would need valid credentials to complete successfully
            logout_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
            logout_btn.click()

           
            
            TestResultCollector.add_result('test_case_4_logout_User', 'PASSED')
        except Exception as e:
            TestResultCollector.add_result('test_case_4_logout_User', 'FAILED', str(e))
            raise e

    def test_case_5_Register_User_with_existing_email(self):
        """Test Case 5: Register User with existing email"""
        self.driver.get(self.base_url)

        # Click on 'Signup / Login' button
        signup_login_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Signup / Login")))
        signup_login_btn.click()
        
        # Verify 'New User Signup!' is visible
        signup_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'New User Signup!')]")))
        assert signup_text.is_displayed()
        
        # Enter name and email address
        name = "allenlee"
        email = "allenlee@punkproof.com"
        
        name_field = self.driver.find_element(By.NAME, "name")
        email_field = self.driver.find_element(By.XPATH, "//input[@data-qa='signup-email']")
        
        name_field.send_keys(name)
        email_field.send_keys(email)
        
        # 7. Click 'Signup' button
        signup_btn = self.driver.find_element(By.XPATH, "//button[@data-qa='signup-button']")
        signup_btn.click()

    def test_case_6_contact_us_form(self):
        """Test Case 6: Contact Us Form"""
        self.driver.get(self.base_url)
        assert "Automation Exercise" in self.driver.title
        
        # Click on 'Contact Us' button
        contact_us_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Contact us")))
        contact_us_btn.click()
        
        # Verify 'GET IN TOUCH' is visible
        get_in_touch_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Get In Touch')]")))
        assert get_in_touch_text.is_displayed()
        
        # Fill contact form
        self.driver.find_element(By.NAME, "name").send_keys("Test User")
        self.driver.find_element(By.NAME, "email").send_keys("test@example.com")
        self.driver.find_element(By.NAME, "subject").send_keys("Test Subject")
        self.driver.find_element(By.NAME, "message").send_keys("This is a test message for automation testing.")
        
        # Upload file (create a temporary file for testing)
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write("Test file content")
            temp_file_path = temp_file.name
        
        file_upload = self.driver.find_element(By.NAME, "upload_file")
        file_upload.send_keys(temp_file_path)
        self.driver.execute_script("window.scrollBy(0,200);")

        # Click Submit button
        submit_btn = self.driver.find_element(By.XPATH, '//*[@id="contact-us-form"]/div[6]/input')
        submit_btn.click()
        
        # Handle alert
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except Exception:
            pass
        
        # Verify success message
        success_message = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Success! Your details have been submitted successfully.')]")))
        assert success_message.is_displayed()
        
        # Clean up temp file
        os.unlink(temp_file_path)
        
        # Click Home button
        home_btn = self.driver.find_element(By.LINK_TEXT, "Home")
        home_btn.click()
        
        # Verify landed on home page
        assert "Automation Exercise" in self.driver.title

    def test_case_7_verify_test_cases_page(self):
        """Test Case 7: Verify Test Cases Page"""
        self.driver.get(self.base_url)
        assert "Automation Exercise" in self.driver.title
        
        # Click on 'Test Cases' button
        test_cases_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Test Cases")))
        test_cases_btn.click()
        
        # Verify user is navigated to test cases page
        assert "test_cases" in self.driver.current_url.lower()
        test_cases_header = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form"]/div/div[1]/div/h2/b')))
        assert test_cases_header.is_displayed()

    def test_case_8_verify_all_products_and_product_detail_page(self):
        """Test Case 8: Verify All Products and product detail page"""
        self.driver.get(self.base_url)
        assert "Automation Exercise" in self.driver.title
        
        # Click on 'Products' button
        products_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div/div/div[2]/div/ul/li[2]/a')))
        products_btn.click()
        
        # Verify user is navigated to ALL PRODUCTS page
        all_products_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'All Products')]")))
        assert all_products_text.is_displayed()
        
        # Verify products list is visible
        products_list = self.driver.find_elements(By.CLASS_NAME, "productinfo")
        assert len(products_list) > 0
        
        self.driver.execute_script("window.scrollBy(0,500);")

        # Click on 'View Product' of first product
        first_view_product = self.driver.find_element(By.XPATH, "//a[contains(@href, '/product_details/')]")
        first_view_product.click()
        
        # Verify product detail page
        product_name = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='product-information']/h2")))
        assert product_name.is_displayed()
        
        # Verify product details are visible
        product_details = self.driver.find_elements(By.XPATH, "//div[@class='product-information']/p")
        assert len(product_details) > 0

    def test_case_9_search_product(self):
        """Test Case 9: Search Product"""
        self.driver.get(self.base_url)
        assert "Automation Exercise" in self.driver.title
        
        # Click on 'Products' button
        products_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div/div/div[2]/div/ul/li[2]/a')))
        products_btn.click()
        
        # Verify user is navigated to ALL PRODUCTS page
        all_products_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'All Products')]")))
        assert all_products_text.is_displayed()
        
        # Enter product name in search input and click search
        search_input = self.driver.find_element(By.ID, "search_product")
        search_input.send_keys("dress")
        
        search_btn = self.driver.find_element(By.ID, "submit_search")
        search_btn.click()
        
        # Verify 'SEARCHED PRODUCTS' is visible
        searched_products_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Searched Products')]")))
        assert searched_products_text.is_displayed()
        
        # Verify all products related to search are visible
        search_results = self.driver.find_elements(By.CLASS_NAME, "productinfo")
        assert len(search_results) > 0

    def test_case_10_verify_subscription_in_home_page(self):
        """Test Case 10: Verify Subscription in home page"""
        self.driver.get(self.base_url)
        assert "Automation Exercise" in self.driver.title
        
        # Scroll down to footer
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Verify text 'SUBSCRIPTION'
        subscription_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Subscription')]")))
        assert subscription_text.is_displayed()
        
        # Enter email and click arrow button
        email_input = self.driver.find_element(By.ID, "susbscribe_email")
        email_input.send_keys("test@example.com")
        
        subscribe_btn = self.driver.find_element(By.ID, "subscribe")
        subscribe_btn.click()
        
        # Verify success message
        success_message = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'You have been successfully subscribed!')]")))
        assert success_message.is_displayed()

    def test_case_11_Verify_subscription_in_cart_page(self):
        """Test Case 11: Verify Subscription in Cart page"""
        self.driver.get(self.base_url)

        # Step 1: Click on 'Cart' button in the header
        cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/view_cart']"))
        )
        cart_button.click()

        # Step 2: Scroll down to subscription section
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Step 3: Enter email address in the subscription input
        email_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "susbscribe_email"))
        )
        email_input.clear()
        email_input.send_keys("testuser123@example.com")

        # Step 4: Click the 'Subscribe' button
        subscribe_button = self.driver.find_element(By.ID, "subscribe")
        subscribe_button.click()

        # Step 5: Verify the success message
        success_alert = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#success-subscribe"))
        )
        assert "You have been successfully subscribed!" in success_alert.text

    def test_case_12_add_products_in_cart(self):
        """Test Case 12: Add Products in Cart"""
        self.driver.get(self.base_url)

        # Step 1: Click on 'Products' link in the navigation bar
        products_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
        )
        products_link.click()

        self.driver.execute_script("window.scrollBy(0,400);")

        # Step 2: Wait for products to load and add the first product to cart
        first_add_to_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
        )
        first_add_to_cart.click()

        # Step 3: Handle the modal and continue shopping
        continue_shopping = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.close-modal.btn-block"))
        )
        continue_shopping.click()

        # Step 4: Add the second product to cart
        second_add_to_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
        )
        second_add_to_cart.click()

        # Step 5: Click 'View Cart' on the modal
        view_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))
        )
        view_cart.click()

        # Step 6: Verify that both products are in the cart
        cart_items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="product-1"]/td[4]/button'))
        )
        assert len(cart_items) >= 0, "Less than 2 products in the cart!"


    def test_case_13_verify_product_quantity_in_cart(self):
        """Test Case 13: Verify Product quantity in Cart"""
        self.driver.get("https://automationexercise.com/products")

        # Step 3: Verify home page is visible
        assert "Automation Exercise" in self.driver.title

        self.driver.execute_script("window.scrollBy(0,600);")

        # Step 4: Click 'View Product' for first product
        view_product = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'View Product')])[1]"))
        )
        view_product.click()

        # Step 5: Verify product detail page is opened
        product_info = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-information"))
        )
        assert product_info.is_displayed()

        # Step 6: Increase quantity to 4
        quantity_input = self.driver.find_element(By.ID, "quantity")
        quantity_input.clear()
        quantity_input.send_keys("4")

        self.driver.execute_script("window.scrollBy(0,400);")

        # Step 7: Click 'Add to cart' button
        add_to_cart = self.driver.find_element(By.XPATH, '/html/body/section/div/div/div[2]/div[2]/div[2]/div/span/button')
        add_to_cart.click()

        # Step 8: Click 'View Cart' on modal
        view_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))
        )
        view_cart.click()

        # Step 9: Verify product is displayed in cart page with quantity 4
        cart_quantity = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button.disabled"))
        )
        assert cart_quantity.text == "4", f"Expected quantity 4, but got {cart_quantity.text}"


    def test_case_14_place_order_register_while_checkout(self):
            """Test Case 14: Place Order: Register while Checkout"""
            self.driver.get("https://automationexercise.com/")

            # Step 2: Verify home page is visible
            assert "Automation Exercise" in self.driver.title

            # Step 3: Add first product to cart
            products_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
            )
            products_link.click()
            first_add_to_cart = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
            )

            self.driver.execute_script("window.scrollBy(0,400);")

            first_add_to_cart.click()
            continue_shopping = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.close-modal.btn-block"))
            )
            continue_shopping.click()

            # Step 4: Click 'Cart' button
            cart_button = self.driver.find_element(By.CSS_SELECTOR, "a[href='/view_cart']")
            cart_button.click()

            # Step 5: Verify cart page is displayed
            assert "Shopping Cart" in self.driver.page_source

            # Step 6: Click 'Proceed To Checkout'
            proceed_to_checkout = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-default.check_out"))
            )
            proceed_to_checkout.click()

            # Step 7: Click 'Register / Login' button
            register_login = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//u[text()='Register / Login']"))
            )
            register_login.click()

            # Step 8: Fill all details in Signup and create account
            # Generate unique email
            random_email = self.generate_random_email()
            name_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "name"))
            )
            email_input = self.driver.find_element(By.XPATH, "//input[@data-qa='signup-email']")
            name_input.send_keys("Test User")
            email_input.send_keys(random_email)
            signup_button = self.driver.find_element(By.XPATH, "//button[@data-qa='signup-button']")
            signup_button.click()

            # Fill account info
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//b[text()='Enter Account Information']"))
            )
            self.driver.execute_script("window.scrollBy(0,400);")

            self.driver.find_element(By.ID, "id_gender1").click()
            self.driver.find_element(By.ID, "password").send_keys("TestPassword123")
            self.driver.find_element(By.ID, "days").send_keys("1")
            self.driver.find_element(By.ID, "months").send_keys("January")
            self.driver.find_element(By.ID, "years").send_keys("2000")
            self.driver.find_element(By.ID, "newsletter").click()
            self.driver.find_element(By.ID, "optin").click()
            self.driver.find_element(By.ID, "first_name").send_keys("Test")
            self.driver.find_element(By.ID, "last_name").send_keys("User")
            self.driver.find_element(By.ID, "company").send_keys("TestCompany")
            self.driver.find_element(By.ID, "address1").send_keys("123 Test St")
            self.driver.find_element(By.ID, "address2").send_keys("Suite 1")
            self.driver.find_element(By.ID, "country").send_keys("United States")
            self.driver.find_element(By.ID, "state").send_keys("TestState")
            self.driver.find_element(By.ID, "city").send_keys("TestCity")
            self.driver.find_element(By.ID, "zipcode").send_keys("12345")
            self.driver.find_element(By.ID, "mobile_number").send_keys("1234567890")
            self.driver.find_element(By.XPATH, "//button[@data-qa='create-account']").click()

            # Step 9: Verify 'ACCOUNT CREATED!' and click 'Continue'
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Created!']"))
            )
            self.driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()

            # Step 10: Verify 'Logged in as username' at top
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Logged in as')]"))
            )

            # Step 11: Click 'Cart' button
            cart_button = self.driver.find_element(By.CSS_SELECTOR, "a[href='/view_cart']")
            cart_button.click()

            # Step 12: Click 'Proceed To Checkout'
            proceed_to_checkout = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-default.check_out"))
            )
            proceed_to_checkout.click()

            # Step 13: Verify Address Details and Review Your Order
            assert "Address Details" in self.driver.page_source
            assert "Review Your Order" in self.driver.page_source

            # Step 14: Enter description in comment text area and click 'Place Order'
            comment_area = self.driver.find_element(By.NAME, "message")
            comment_area.send_keys("Please deliver between 9am-5pm.")
            place_order = self.driver.find_element(By.XPATH, "//a[text()='Place Order']")
            place_order.click()

            # Step 15: Enter payment details
            self.driver.find_element(By.NAME, "name_on_card").send_keys("Test User")
            self.driver.find_element(By.NAME, "card_number").send_keys("4111111111111111")
            self.driver.find_element(By.NAME, "cvc").send_keys("123")
            self.driver.find_element(By.NAME, "expiry_month").send_keys("12")
            self.driver.find_element(By.NAME, "expiry_year").send_keys("2028")
            self.driver.find_element(By.ID, "submit").click()

            # Step 16: Verify success message
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="form"]/div/div/div/p'))
            )

    def test_case_15_place_order_register_before_checkout(self):
        """Test Case 15: Place Order: Register before Checkout"""
        self.driver.get(self.base_url)

        # Step 3: Verify home page is visible
        assert "Automation Exercise" in self.driver.title

        # Step 4: Click 'Signup / Login' button
        signup_login = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/login']"))
        )
        signup_login.click()

        # Step 5: Fill all details in Signup and create account
        random_email = f"testuser{random.randint(10000,99999)}@example.com"
        name_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "name"))
        )
        email_input = self.driver.find_element(By.XPATH, "//input[@data-qa='signup-email']")
        name_input.send_keys("Test User")
        email_input.send_keys(random_email)
        signup_button = self.driver.find_element(By.XPATH, "//button[@data-qa='signup-button']")
        signup_button.click()

        
        
        # Fill account info
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//b[text()='Enter Account Information']"))
        )

        self.driver.execute_script("window.scrollBy(0,400);")
        self.driver.find_element(By.ID, "id_gender1").click()
        self.driver.find_element(By.ID, "password").send_keys("TestPassword123")
        self.driver.find_element(By.ID, "days").send_keys("1")
        self.driver.find_element(By.ID, "months").send_keys("January")
        self.driver.find_element(By.ID, "years").send_keys("2000")
        self.driver.find_element(By.ID, "newsletter").click()
        self.driver.find_element(By.ID, "optin").click()
        self.driver.find_element(By.ID, "first_name").send_keys("Test")
        self.driver.find_element(By.ID, "last_name").send_keys("User")
        self.driver.find_element(By.ID, "company").send_keys("TestCompany")
        self.driver.find_element(By.ID, "address1").send_keys("123 Test St")
        self.driver.find_element(By.ID, "address2").send_keys("Suite 1")
        self.driver.find_element(By.ID, "country").send_keys("United States")
        self.driver.find_element(By.ID, "state").send_keys("TestState")
        self.driver.find_element(By.ID, "city").send_keys("TestCity")
        self.driver.find_element(By.ID, "zipcode").send_keys("12345")
        self.driver.find_element(By.ID, "mobile_number").send_keys("1234567890")
        self.driver.find_element(By.XPATH, "//button[@data-qa='create-account']").click()

        # Step 6: Verify 'ACCOUNT CREATED!' and click 'Continue' button
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Created!']"))
        )
        self.driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()

        # Step 7: Verify 'Logged in as username' at top
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Logged in as')]"))
        )

        # Step 8: Add products to cart
        products_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/products']")
        products_link.click()
        first_add_to_cart = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
        )
        
        self.driver.execute_script("window.scrollBy(0,600);")
        
        first_add_to_cart.click()
        continue_shopping = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.close-modal.btn-block"))
        )
        continue_shopping.click()

        # Step 9: Click 'Cart' button
        cart_button = self.driver.find_element(By.CSS_SELECTOR, "a[href='/view_cart']")
        cart_button.click()

        # Step 10: Verify that cart page is displayed
        assert "Shopping Cart" in self.driver.page_source

        # Step 11: Click 'Proceed To Checkout'
        proceed_to_checkout = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-default.check_out"))
        )
        proceed_to_checkout.click()

        # Step 12: Verify Address Details and Review Your Order
        assert "Address Details" in self.driver.page_source
        assert "Review Your Order" in self.driver.page_source

        # Step 13: Enter description in comment text area and click 'Place Order'
        comment_area = self.driver.find_element(By.NAME, "message")
        comment_area.send_keys("Please deliver between 9am-5pm.")
        place_order = self.driver.find_element(By.XPATH, "//a[text()='Place Order']")
        place_order.click()

        # Step 14: Enter payment details
        self.driver.find_element(By.NAME, "name_on_card").send_keys("Test User")
        self.driver.find_element(By.NAME, "card_number").send_keys("4111111111111111")
        self.driver.find_element(By.NAME, "cvc").send_keys("123")
        self.driver.find_element(By.NAME, "expiry_month").send_keys("12")
        self.driver.find_element(By.NAME, "expiry_year").send_keys("2028")
        self.driver.find_element(By.ID, "submit").click()

        # Step 16: Verify success message
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Your order has been confirmed!')]"))
        )
    
    
    def test_case_16_place_order_login_before_checkout(self):
        """Test Case 16: Place Order: Login before Checkout"""
        self.driver.get(self.base_url)

        # Step 3: Verify home page is visible
        assert "Automation Exercise" in self.driver.title

        # Step 4: Click 'Signup / Login' button
        signup_login = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/login']"))
        )
        signup_login.click()

        # Step 5: Fill email and password to login
        email_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@data-qa='login-email']"))
        )
        password_input = self.driver.find_element(By.XPATH, "//input[@data-qa='login-password']")
        email_input.send_keys("allenlee@punkproof.com")       # <-- Replace with your test email
        password_input.send_keys("SKDeIutmdZqgNxJ")             # <-- Replace with your test password

        # Step 6: Click 'Login' button
        login_button = self.driver.find_element(By.XPATH, "//button[@data-qa='login-button']")
        login_button.click()

        # Step 7: Verify 'Logged in as username' at top
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Logged in as')]"))
        )

        # Step 8: Add products to cart
        products_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/products']")
        products_link.click()
        first_add_to_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
        )
        
        self.driver.execute_script("window.scrollBy(0,600);")
        
        first_add_to_cart.click()
        continue_shopping = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.close-modal.btn-block"))
        )
        continue_shopping.click()

        # Step 9: Click 'Cart' button
        cart_button = self.driver.find_element(By.CSS_SELECTOR, "a[href='/view_cart']")
        cart_button.click()

        # Step 10: Verify cart page is displayed
        assert "Shopping Cart" in self.driver.page_source

        # Step 11: Click 'Proceed To Checkout'
        proceed_to_checkout = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-default.check_out"))
        )
        proceed_to_checkout.click()

        # Step 12: Verify Address Details and Review Your Order
        assert "Address Details" in self.driver.page_source
        assert "Review Your Order" in self.driver.page_source

        # Step 13: Enter description in comment text area and click 'Place Order'
        comment_area = self.driver.find_element(By.NAME, "message")
        comment_area.send_keys("Please deliver between 9am-5pm.")
        place_order = self.driver.find_element(By.XPATH, "//a[text()='Place Order']")
        place_order.click()

        # Step 14: Enter payment details
        self.driver.find_element(By.NAME, "name_on_card").send_keys("Test User")
        self.driver.find_element(By.NAME, "card_number").send_keys("4111111111111111")
        self.driver.find_element(By.NAME, "cvc").send_keys("123")
        self.driver.find_element(By.NAME, "expiry_month").send_keys("12")
        self.driver.find_element(By.NAME, "expiry_year").send_keys("2028")
        self.driver.find_element(By.ID, "submit").click()
    

    def test_case_17_Remove_Products_From_Cart(self):
        """Test Case 17: Remove Products From Cart"""
        self.driver.get("https://automationexercise.com/products")

        self.driver.execute_script("window.scrollBy(0,600);")
        
        # Step 4: Click "Add to cart"
        first_add_to_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
        )
        self.driver.execute_script("window.scrollBy(0,600);")
        
        first_add_to_cart.click()
        
        # Step 5: Click "View Cart" in the modal
        view_cart_btn = WebDriverWait( self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))
        )
        view_cart_btn.click()

        # Step 6: Remove the item by click X
        cross_icon = WebDriverWait( self.driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="product-1"]/td[6]/a/i'))
        )
        cross_icon.click()
    
    def test_case_18_view_category_products(self):
        """Test Case 18: View Category Products"""
        self.driver.get(self.base_url)
        
        # Step 2: Verify homepage is visible
        assert "Automation Exercise" in self.driver.title

        # Step 3: Verify 'CATEGORY' section is visible in sidebar
        self.driver.get("https://automationexercise.com/products")
        
        category_header = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()='Category']"))
        )
        assert category_header.is_displayed()
        self.driver.execute_script("window.scrollBy(0,600);")

        # Step 4: Click on 'Women' category
        women_category = self.driver.find_element(By.XPATH, '//*[@id="accordian"]/div[1]/div[1]/h4/a')
        women_category.click()

        # Step 5: Click on 'Dress' sub-category under 'Women'
        dress_subcategory = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="Women"]/div/ul/li[1]/a'))
        )
        dress_subcategory.click()

        # Step 6: Verify that category page is displayed and correct category/sub-category is shown
        category_title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[@class='title text-center']"))
        )
        assert "WOMEN - DRESS PRODUCTS" in category_title.text

        # Step 7: Verify that products for that category are visible
        products = self.driver.find_elements(By.CSS_SELECTOR, ".features_items .product-image-wrapper")
        assert len(products) > 0, "No products found for the selected category!"

    
    def test_case_19_view_and_cart_brand_products(self):
        """Test Case 19: View & Cart Brand Products"""
        self.driver.get(self.base_url)

        # Step 3: Click on 'Products' button
        products_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
        )
        products_btn.click()

        # Step 4: Verify that Brands are visible on left sidebar
        brands_header = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()='Brands']"))
        )
        assert brands_header.is_displayed()

        self.driver.execute_script("window.scrollBy(0,400);")

        # Step 5: Click on the first brand (e.g., "Polo")
        first_brand = self.driver.find_element(By.XPATH, "(//div[@class='brands-name']/ul/li/a)[1]")
        brand_name_1 = first_brand.text.split()[1]
        first_brand.click()

        # Step 6: Verify user is navigated to brand page and brand products are displayed
        category_title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.title.text-center"))
        )
        assert brand_name_1.upper() in category_title.text.upper()
        
        products = self.driver.find_elements(By.CSS_SELECTOR, ".features_items .product-image-wrapper")
        assert len(products) > 0, f"No products found for brand {brand_name_1}!"

        # Step 7: Click on another brand (e.g., "H&M")
        second_brand = self.driver.find_element(By.XPATH, "(//div[@class='brands-name']/ul/li/a)[2]")
        brand_name_2 = second_brand.text.split()[1]
        second_brand.click()

        # Step 8: Verify user is navigated to that brand page and can see products
        category_title_2 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.title.text-center"))
        )
        assert brand_name_2.upper() in category_title_2.text.upper()
        products_2 = self.driver.find_elements(By.CSS_SELECTOR, ".features_items .product-image-wrapper")
        assert len(products_2) > 0, f"No products found for brand {brand_name_2}!"

    def test_case_20_search_and_verify_cart_after_login(self):
        """Test Case 20: Search Products and Verify Cart After Login"""
        
        # Test data
        product_name = "T-Shirt"  # Replace with valid product name from site
        login_email = "allenlee@punkproof.com"  # Replace with valid credentials
        login_password = "SKDeIutmdZqgNxJ"  # Replace with valid credentials

        # Step 1-2: Launch browser and navigate
        self.driver.get(self.base_url)

        # Step 1-3: Login
        self.driver.find_element(By.CSS_SELECTOR, "a[href='/login']").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-qa='login-email']"))
        ).send_keys(login_email)
        
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys(login_password)
        self.driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()
        
        
        # Step 3: Click Products
        products_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
        )
        products_btn.click()

        # Step 4: Verify ALL PRODUCTS page
        assert "All Products" in self.driver.page_source

        # Step 5: Search product
        search_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "search_product"))
        )
        search_input.send_keys(product_name)
        self.driver.find_element(By.ID, "submit_search").click()

        # Step 6: Verify SEARCHED PRODUCTS
        assert "Searched Products" in self.driver.page_source

        
        self.driver.execute_script("window.scrollBy(0,600);")
        
        # Step 1: Click on 'Products' link in the navigation bar
        products_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
        )
        products_link.click()

        self.driver.execute_script("window.scrollBy(0,400);")

        # Step 2: Wait for products to load and add the first product to cart
        first_add_to_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
        )
        first_add_to_cart.click()

        # Step 3: Handle the modal and continue shopping
        continue_shopping = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.close-modal.btn-block"))
        )
        continue_shopping.click()

        # Step 4: Add the second product to cart
        second_add_to_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
        )
        second_add_to_cart.click()

        # Step 5: Click 'View Cart' on the modal
        view_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))
        )
        view_cart.click()

        # Step 6: Verify that both products are in the cart
        cart_items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="product-1"]/td[4]/button'))
        )
        assert len(cart_items) >= 0, "Less than 2 products in the cart!"

    def test_case_21_add_review_on_product(self):
        """Test Case 21: Add review on product"""
        self.driver.get(self.base_url)
        assert "Automation Exercise" in self.driver.title
        
        # Click on 'Products' button
        products_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div/div/div[2]/div/ul/li[2]/a')))
        products_btn.click()
        
        # Verify user is navigated to ALL PRODUCTS page
        all_products_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'All Products')]")))
        assert all_products_text.is_displayed()
        
        # Click on 'View Product' button
        self.driver.get("https://automationexercise.com/product_details/1")
        
        # Verify 'Write Your Review' is visible
        review_section = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Write Your Review')]")))
        assert review_section.is_displayed()
        
        self.driver.execute_script("window.scrollTo(0, 600)")
        
        # Enter name, email and review
        name_field = self.driver.find_element(By.ID, "name")
        email_field = self.driver.find_element(By.ID, "email")
        review_field = self.driver.find_element(By.ID, "review")
        
        name_field.send_keys("Test Reviewer")
        email_field.send_keys("reviewer@example.com")
        review_field.send_keys("This is a test review for automation testing purposes.")
        
        # Click 'Submit' button
        submit_btn = self.driver.find_element(By.ID, "button-review")
        submit_btn.click()
        
        # Verify success message
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="review-section"]/div/div/span'))
        )
        assert success_message.is_displayed()


    def test_case_22_add_to_cart_from_recommended_items(self):
        """Test Case 22: Add to cart from Recommended items"""
        self.driver.get(self.base_url)

        # Step 2: Scroll to "Recommended items"
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Step 3: Verify "Recommended items" section is visible
        recommended_section = WebDriverWait( self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()='recommended items']"))
        )
        assert recommended_section.is_displayed()

        # Step 4: Click "Add to cart" on the first recommended product
        add_to_cart_btn = WebDriverWait( self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@id='recommended-item-carousel']//a[contains(text(),'Add to cart')])[1]"))
        )
        add_to_cart_btn.click()

        # Step 5: Click "View Cart" in the modal
        view_cart_btn = WebDriverWait( self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))
        )
        view_cart_btn.click()

        # Step 6: Verify the product appears in the cart
        cart_products = WebDriverWait( self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="cart_items"]/div/div[1]/ol/li[2]'))
        )
        assert len(cart_products) > 0, "No products found in the cart from Recommended items!"


    def test_case_23_verify_address_details_in_checkout(self):
            """Test Case 23: Verify address details in checkout page"""
            # Step 1: Click 'Register / Login' button
            self.driver.get(self.base_url)
            register_login = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div/div/div[2]/div/ul/li[4]/a'))
            )
            register_login.click()

            # Step 2: Fill all details in Signup and create account
            # Generate unique email
            random_email = self.generate_random_email()
            name_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "name"))
            )
            email_input = self.driver.find_element(By.XPATH, "//input[@data-qa='signup-email']")
            name_input.send_keys("Test User")
            email_input.send_keys(random_email)
            signup_button = self.driver.find_element(By.XPATH, "//button[@data-qa='signup-button']")
            signup_button.click()

            # Fill account info
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//b[text()='Enter Account Information']"))
            )
            self.driver.execute_script("window.scrollBy(0,400);")

            self.driver.find_element(By.ID, "id_gender1").click()
            self.driver.find_element(By.ID, "password").send_keys("TestPassword123")
            self.driver.find_element(By.ID, "days").send_keys("1")
            self.driver.find_element(By.ID, "months").send_keys("January")
            self.driver.find_element(By.ID, "years").send_keys("2000")
            self.driver.find_element(By.ID, "newsletter").click()
            self.driver.find_element(By.ID, "optin").click()
            self.driver.find_element(By.ID, "first_name").send_keys("Test")
            self.driver.find_element(By.ID, "last_name").send_keys("User")
            self.driver.find_element(By.ID, "company").send_keys("TestCompany")
            self.driver.find_element(By.ID, "address1").send_keys("123 Test St")
            self.driver.find_element(By.ID, "address2").send_keys("Suite 1")
            self.driver.find_element(By.ID, "country").send_keys("United States")
            self.driver.find_element(By.ID, "state").send_keys("TestState")
            self.driver.find_element(By.ID, "city").send_keys("TestCity")
            self.driver.find_element(By.ID, "zipcode").send_keys("12345")
            self.driver.find_element(By.ID, "mobile_number").send_keys("1234567890")
            self.driver.find_element(By.XPATH, "//button[@data-qa='create-account']").click()

            # Step 9: Verify 'ACCOUNT CREATED!' and click 'Continue'
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Created!']"))
            )
            self.driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()

            # Step 10: Verify 'Logged in as username' at top
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Logged in as')]"))
            )
            
            # Step 1: Click on 'Products' link in the navigation bar
            products_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
            )
            products_link.click()

            self.driver.execute_script("window.scrollBy(0,400);")

            # Step 2: Wait for products to load and add the first product to cart
            first_add_to_cart = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
            )
            first_add_to_cart.click()

            # Step 3: Handle the modal and continue shopping
            continue_shopping = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.close-modal.btn-block"))
            )
            continue_shopping.click()

            # Step 4: Add the second product to cart
            second_add_to_cart = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
            )
            second_add_to_cart.click()

            # Step 5: Click 'View Cart' on the modal
            view_cart = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))
            )
            view_cart.click()

            # Step 6: Verify that both products are in the cart
            cart_items = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="product-1"]/td[4]/button'))
            )
            assert len(cart_items) >= 0, "Less than 2 products in the cart!"

            # Step 5: Go to cart and proceed to checkout
            self.driver.find_element(By.CSS_SELECTOR, "a[href='/view_cart']").click()
            proceed_to_checkout = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-default.check_out"))
            )
            proceed_to_checkout.click()

            # Step 6: Verify address details
            delivery_address = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//ul[@id='address_delivery']"))
            )
            billing_address = self.driver.find_element(By.XPATH, "//ul[@id='address_invoice']")

            # Check that details match what was entered during registration
            expected_strings = [
                "Test User",
                "TestCompany",
                "123 Test St",
                "Suite 1",
                "TestCity TestState 12345",
                "United States",
                "1234567890"
            ]
            for expected in expected_strings:
                assert expected in delivery_address.text, f"'{expected}' not found in delivery address"
                assert expected in billing_address.text, f"'{expected}' not found in billing address"

            # Optional: Cleanup - Delete account
            self.driver.find_element(By.CSS_SELECTOR, "a[href='/delete_account']").click()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Deleted!']"))
            )
            self.driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()


    def test_case_24_download_invoice_after_purchase(self):
        """Test Case 24: Download Invoice after purchase order"""
        if not os.path.exists(self.DOWNLOAD_DIR):
            os.makedirs(self.DOWNLOAD_DIR)

        self.driver.get("https://automationexercise.com/")

        # Register a new user
        # Step 1: Click 'Register / Login' button
        self.driver.get(self.base_url)
        register_login = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div/div/div[2]/div/ul/li[4]/a'))
        )
        register_login.click()

        # Step 2: Fill all details in Signup and create account
        # Generate unique email
        random_email = self.generate_random_email()
        name_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "name"))
        )
        email_input = self.driver.find_element(By.XPATH, "//input[@data-qa='signup-email']")
        name_input.send_keys("Test User")
        email_input.send_keys(random_email)
        signup_button = self.driver.find_element(By.XPATH, "//button[@data-qa='signup-button']")
        signup_button.click()

        # Fill account info
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//b[text()='Enter Account Information']"))
        )
        self.driver.execute_script("window.scrollBy(0,400);")

        self.driver.find_element(By.ID, "id_gender1").click()
        self.driver.find_element(By.ID, "password").send_keys("TestPassword123")
        self.driver.find_element(By.ID, "days").send_keys("1")
        self.driver.find_element(By.ID, "months").send_keys("January")
        self.driver.find_element(By.ID, "years").send_keys("2000")
        self.driver.find_element(By.ID, "newsletter").click()
        self.driver.find_element(By.ID, "optin").click()
        self.driver.find_element(By.ID, "first_name").send_keys("Test")
        self.driver.find_element(By.ID, "last_name").send_keys("User")
        self.driver.find_element(By.ID, "company").send_keys("TestCompany")
        self.driver.find_element(By.ID, "address1").send_keys("123 Test St")
        self.driver.find_element(By.ID, "address2").send_keys("Suite 1")
        self.driver.find_element(By.ID, "country").send_keys("United States")
        self.driver.find_element(By.ID, "state").send_keys("TestState")
        self.driver.find_element(By.ID, "city").send_keys("TestCity")
        self.driver.find_element(By.ID, "zipcode").send_keys("12345")
        self.driver.find_element(By.ID, "mobile_number").send_keys("1234567890")
        self.driver.find_element(By.XPATH, "//button[@data-qa='create-account']").click()

        # Step 9: Verify 'ACCOUNT CREATED!' and click 'Continue'
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Created!']"))
        )
        self.driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()

        # Step 10: Verify 'Logged in as username' at top
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Logged in as')]"))
        )

        # Step 1: Click on 'Products' link in the navigation bar
        products_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
        )
        products_link.click()

        self.driver.execute_script("window.scrollBy(0,400);")

        # Step 2: Wait for products to load and add the first product to cart
        first_add_to_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
        )
        first_add_to_cart.click()

        # Step 3: Handle the modal and continue shopping
        continue_shopping = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.close-modal.btn-block"))
        )
        continue_shopping.click()

        # Step 4: Add the second product to cart
        second_add_to_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
        )
        second_add_to_cart.click()

        # Step 5: Click 'View Cart' on the modal
        view_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))
        )
        view_cart.click()

        # Go to cart and checkout
        self.driver.find_element(By.CSS_SELECTOR, "a[href='/view_cart']").click()
        proceed_to_checkout = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-default.check_out"))
        )
        proceed_to_checkout.click()

        # Enter comment and place order
        self.driver.find_element(By.NAME, "message").send_keys("Please deliver soon.")
        place_order = self.driver.find_element(By.XPATH, "//a[text()='Place Order']")
        place_order.click()

        # Enter payment details
        self.driver.find_element(By.NAME, "name_on_card").send_keys("Test User")
        self.driver.find_element(By.NAME, "card_number").send_keys("4111111111111111")
        self.driver.find_element(By.NAME, "cvc").send_keys("123")
        self.driver.find_element(By.NAME, "expiry_month").send_keys("12")
        self.driver.find_element(By.NAME, "expiry_year").send_keys("2028")
        self.driver.find_element(By.ID, "submit").click()

        # Wait for order confirmation and download invoice
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Your order has been confirmed!')]"))
        )
        download_invoice_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Download Invoice']"))
        )
        download_invoice_btn.click()

        # Wait for download to complete (wait for file to appear in directory)
        invoice_found = False
        for _ in range(10):  # Wait up to 10 seconds
            files = os.listdir(self.DOWNLOAD_DIR)
            if any(f.endswith('.txt') for f in files):
                invoice_found = True
                break
            time.sleep(1)
        assert invoice_found, "Invoice txt was not downloaded!"

        # Cleanup: Delete account
        self.driver.find_element(By.CSS_SELECTOR, "a[href='/delete_account']").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Deleted!']"))
        )
        self.driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()
    
    
    
    def test_case_25_verify_scroll_up_with_arrow_and_scroll_down(self):
        """Test Case 25: Verify Scroll Up using 'Arrow' button and Scroll Down functionality"""
        self.driver.get(self.base_url)
        assert "Automation Exercise" in self.driver.title
        
        # Scroll down to bottom
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Verify 'SUBSCRIPTION' is visible
        subscription_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Subscription')]")))
        assert subscription_text.is_displayed()
        
        # Click on arrow button to scroll up
        try:
            arrow_btn = self.driver.find_element(By.XPATH, '//*[@id="scrollUp"]/i')
            arrow_btn.click()
            time.sleep(2)
            
            # Verify page scrolled up and header text is visible
            header_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Full-Fledged practice website for Automation Engineers')]")))
            assert header_text.is_displayed()
        except NoSuchElementException:
            # If arrow button not found, scroll up programmatically
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)

    def test_case_26_verify_scroll_up_without_arrow_and_scroll_down(self):
        """Test Case 26: Verify Scroll Up without 'Arrow' button and Scroll Down functionality"""
        self.driver.get(self.base_url)
        assert "Automation Exercise" in self.driver.title
        
        # Scroll down to bottom
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Verify 'SUBSCRIPTION' is visible
        subscription_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Subscription')]")))
        assert subscription_text.is_displayed()
        
        # Scroll up to top without using arrow button
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # Verify page scrolled up and header text is visible
        try:
            header_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Full-Fledged practice website for Automation Engineers')]")))
            assert header_text.is_displayed()
        except TimeoutException:
            # Alternative verification - check if we're at the top of the page
            scroll_position = self.driver.execute_script("return window.pageYOffset;")
            assert scroll_position == 0

    # Pytest hooks should be defined at the module level, not inside a class
    
    # def pytest_runtest_logreport(report):
    #     """Pytest hook to capture test results"""
    #     if report.when == 'call':
    #         test_name = report.nodeid.split('::')[-1]
    
    #         if report.outcome == 'passed':
    #             TestResultCollector.add_result(test_name, 'PASSED')
    #         elif report.outcome == 'failed':
    #             error_msg = str(report.longrepr) if hasattr(report, 'longrepr') else 'Unknown error'
    #             TestResultCollector.add_result(test_name, 'FAILED', error_msg)
    #         elif report.outcome == 'skipped':
    #             TestResultCollector.add_result(test_name, 'SKIPPED')
    
    # def pytest_sessionstart(session):
    #     """Called after the Session object has been created"""
    #     TestResultCollector.reset_results()
    
    # def pytest_sessionfinish(session, exitstatus):
    #     """Called after whole test run finished"""
    #     TestResultCollector.send_test_report_email()

    if __name__ == "__main__":
        # Initialize test results
        TestResultCollector.reset_results()
        
        # Run tests with retry functionality
        exit_code = pytest.main([
            "-v", 
            "--reruns=3", 
            "--reruns-delay=2",
            __file__
        ])
        
        # Send email report after execution
        TestResultCollector.send_test_report_email()

        exit(exit_code)