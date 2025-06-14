import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Testcase22:
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



    def test_add_to_cart_from_recommended_items(self):
        self.driver.get(self.base_url)

        # Step 2: Scroll to "Recommended items"
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Step 3: Verify "Recommended items" section is visible
        recommended_section = WebDriverWait( self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()='recommended items']"))
        )
        assert recommended_section.is_displayed()

        # Step 4: Click "Add to cart" on the first recommended product
        add_to_cart_btn = WebDriverWait( self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@id='recommended-item-carousel']//a[contains(text(),'Add to cart')])[1]"))
        )
        add_to_cart_btn.click()

        # Step 5: Click "View Cart" in the modal
        view_cart_btn = WebDriverWait( self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))
        )
        view_cart_btn.click()

        # Step 6: Verify the product appears in the cart
        cart_products = WebDriverWait( self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="cart_items"]/div/div[1]/ol/li[2]'))
        )
        assert len(cart_products) > 0, "No products found in the cart from Recommended items!"



if __name__ == "__main__":
        # Run specific test
        pytest.main(["-v", __file__])