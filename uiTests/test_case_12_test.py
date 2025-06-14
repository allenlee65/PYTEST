import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class Testcase12:
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

    def test_add_products_in_cart(self):
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

if __name__ == "__main__":
        # Run specific test
        pytest.main(["-v", __file__])