import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import random
import string



class Testcase01:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method to initialize WebDriver before each test"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option("prefs", { "profile.default_content_setting_values.geolocation": 2})
        ##chrome_options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://automationexercise.com"
        
        yield
        self.driver.quit()
    

    def generate_random_email(self):
            """Generate random email for testing"""
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            return f"test_{random_string}@example.com"
    
    def generate_random_name(self):
            """Generate random name for testing"""
            names = ["John", "Jane", "Mike", "Sarah", "David", "Emma", "Alex", "Lisa"]
            return random.choice(names) + str(random.randint(100, 999))
    
    def test_case_1_register_user(self):
            """Test Case 1: Register User"""
            # 1. Launch browser and navigate to URL

            self.driver.get("http://automationexercise.com")
        

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

if __name__ == "__main__":
    # Run specific test
    pytest.main(["-v", __file__])