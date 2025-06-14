import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Testcase19:
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



    def test_view_and_cart_brand_products(self):
        self.driver.get(self.base_url)

        # Step 3: Click on 'Products' button
        products_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
        )
        products_btn.click()

        # Step 4: Verify that Brands are visible on left sidebar
        brands_header = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()='Brands']"))
        )
        assert brands_header.is_displayed()

        self.driver.execute_script("window.scrollBy(0,400);")

        # Step 5: Click on the first brand (e.g., "Polo")
        first_brand = self.driver.find_element(By.XPATH, "(//div[@class='brands-name']/ul/li/a)[1]")
        brand_name_1 = first_brand.text.split()[1]
        first_brand.click()

        # Step 6: Verify user is navigated to brand page and brand products are displayed
        category_title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.title.text-center"))
        )
        assert brand_name_1.upper() in category_title.text.upper()
        
        products = self.driver.find_elements(By.CSS_SELECTOR, ".features_items .product-image-wrapper")
        assert len(products) > 0, f"No products found for brand {brand_name_1}!"

        # Step 7: Click on another brand (e.g., "H&M")
        second_brand = self.driver.find_element(By.XPATH, "(//div[@class='brands-name']/ul/li/a)[2]")
        brand_name_2 = second_brand.text.split()[1]
        second_brand.click()

        # Step 8: Verify user is navigated to that brand page and can see products
        category_title_2 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.title.text-center"))
        )
        assert brand_name_2.upper() in category_title_2.text.upper()
        products_2 = self.driver.find_elements(By.CSS_SELECTOR, ".features_items .product-image-wrapper")
        assert len(products_2) > 0, f"No products found for brand {brand_name_2}!"


if __name__ == "__main__":
        # Run specific test
        pytest.main(["-v", __file__])