import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class Testcase13:
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

    def test_verify_product_quantity_in_cart(self):
        self.driver.get(self.base_url)

        # Step 3: Verify home page is visible
        assert "Automation Exercise" in self.driver.title

        self.driver.execute_script("window.scrollBy(0,400);")

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

if __name__ == "__main__":
        # Run specific test
        pytest.main(["-v", __file__])