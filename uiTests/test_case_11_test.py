import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class Testcase11:
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
        
        # Teardown
        self.driver.quit()

    def test_subscription_in_cart_page(self):
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

    if __name__ == "__main__":
        # Run specific test
        pytest.main(["-v", __file__])