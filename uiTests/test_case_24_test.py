import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import string
import os
import time



class Testcase24:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method to initialize WebDriver before each test"""
        chrome_options = Options()
        prefs = {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "download.directory_upgrade": True,
            "profile.default_content_setting_values.geolocation": 2
        }
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option("prefs", { "profile.default_content_setting_values.geolocation": 2})
        ##chrome_options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://automationexercise.com"
        self.DOWNLOAD_DIR = "/home/allenlee/Downloads"
        yield
        
        # Teardown
        self.driver.quit()

    def generate_random_email(self):
            """Generate random email for testing"""
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            return f"test_{random_string}@example.com"



    def test_download_invoice_after_purchase(self):
        if not os.path.exists(self.DOWNLOAD_DIR):
            os.makedirs(self.DOWNLOAD_DIR)

        self.driver.get("https://automationexercise.com/")

        # Register a new user
        # Step 1: Click 'Register / Login' button
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



if __name__ == "__main__":
        # Run specific test
        pytest.main(["-v", __file__])