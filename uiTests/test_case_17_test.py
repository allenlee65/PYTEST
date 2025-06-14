import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Testcase17:
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



    def test_case_17_Remove_Products_From_Cart(self):
        
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


if __name__ == "__main__":
        # Run specific test
        pytest.main(["-v", __file__])