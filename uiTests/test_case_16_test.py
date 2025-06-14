import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import string

class Testcase16:
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



    def test_place_order_login_before_checkout(self):
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

        # Step 16: Verify success message
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Your order has been confirmed!')]"))
        )

        # # Step 17: Click 'Delete Account' button
        # delete_account = self.driver.find_element(By.XPATH, "//a[text()='Delete Account']")
        # delete_account.click()

        # # Step 18: Verify 'ACCOUNT DELETED!' and click 'Continue' button
        # WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Deleted!']"))
        # )
        # self.driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()



if __name__ == "__main__":
        # Run specific test
        pytest.main(["-v", __file__])