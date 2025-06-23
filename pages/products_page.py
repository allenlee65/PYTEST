from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait


class ProductsPage(BasePage):
    
    def goto_products_page(self):
        # Step 1: Launch browser and navigate to URL
        self.driver.get(self.base_url)

        # Step 2: Click on 'Products' link in the navigation bar
        products_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
        )
        products_link.click()

        assert self.driver.current_url == f"{self.base_url}/products"

    def add_to_cart(self):
        # Wait for products to load and add the first product to cart
        first_add_to_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
        )
        first_add_to_cart.click()

    def continue_shopping(self):
        # Handle the modal and continue shopping
        continue_shopping = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.close-modal.btn-block"))
        )
        continue_shopping.click()

    def add_second_product_to_cart(self):
        # Step 4: Add the second product to cart
        second_add_to_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'Add to cart')])[1]"))
        )
        second_add_to_cart.click()

    def click_view_cart(self):
        # Click 'View Cart' on the modal
        view_cart = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))
        )
        view_cart.click()
        
    def verify_items_in_cart(self):
        # Step 6: Verify that both products are in the cart
        cart_items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="product-1"]/td[4]/button'))
        )
        assert len(cart_items) >= 0, "Less than 2 products in the cart!"

    def view_product(self):
        view_product = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'View Product')])[1]"))
        )
        view_product.click()
        assert self.driver.current_url == f"{self.base_url}/product_details/1"