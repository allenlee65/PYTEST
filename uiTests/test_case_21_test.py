import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Testcase21:
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
        
        
    def test_case_21(self):
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
        #success_message = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Thank you for your review')]")))
        

        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="review-section"]/div/div/span'))
        )
        assert success_message.is_displayed()


if __name__ == "__main__":
        # Run specific test
        pytest.main(["-v", __file__])