import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import string

class Testcase14:
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

    def generate_random_email(self):
            """Generate random email for testing"""
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            return f"test_{random_string}@example.com"


    def test_place_order_register_while_checkout(self):
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


if __name__ == "__main__":
        # Run specific test
        pytest.main(["-v", __file__])