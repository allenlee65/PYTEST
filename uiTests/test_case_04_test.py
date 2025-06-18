import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



class Testcase04:
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
    

    def test_case_4_logout_User(self):
        """Test Case 4: Logout User"""
        # Note: This test requires pre-existing account credentials
        # For demo purposes, using placeholder credentials
        
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

        assert "login" in self.driver.current_url

if __name__ == "__main__":
    # Run specific test
    pytest.main(["-v", __file__])