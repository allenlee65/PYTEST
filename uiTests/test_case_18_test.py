import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Testcase18:
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



    def test_view_category_products(self):
        self.driver.get(self.base_url)

        # Step 2: Verify homepage is visible
        assert "Automation Exercise" in self.driver.title

        self.driver.get("https://automationexercise.com/products")
        self.driver.execute_script("window.scrollBy(0,600);")

        # Step 3: Verify 'CATEGORY' section is visible in sidebar
        category_header = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()='Category']"))
        )
        assert category_header.is_displayed()

        # Step 4: Click on 'Women' category
        women_category = self.driver.find_element(By.XPATH, "//a[@href='#Women']")
        women_category.click()

        # Step 5: Click on 'Dress' sub-category under 'Women'
        dress_subcategory = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="Women"]/div/ul/li[1]/a'))
        )
        dress_subcategory.click()

        # Step 6: Verify that category page is displayed and correct category/sub-category is shown
        category_title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[@class='title text-center']"))
        )
        assert "WOMEN - DRESS PRODUCTS" in category_title.text

        # Step 7: Verify that products for that category are visible
        products = self.driver.find_elements(By.CSS_SELECTOR, ".features_items .product-image-wrapper")
        assert len(products) > 0, "No products found for the selected category!"



if __name__ == "__main__":
        # Run specific test
        pytest.main(["-v", __file__])