from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class SignUp(BasePage):
    
    def signUp(self):
        """Test Case 1: Register User"""
        # 1. Launch browser and navigate to URL
        self.driver.get(self.base_url)
        
        # 3. Verify home page is visible
        assert "Automation Exercise" in self.driver.title
        
        # 4. Click on 'Signup / Login' button
        signup_login_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Signup / Login")))
        signup_login_btn.click()
        
        # 5. Verify 'New User Signup!' is visible
        signup_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'New User Signup!')]")))
        assert signup_text.is_displayed()
        
        # 6. Enter name and email address
        username = self.generate_random_name()
        email = self.generate_random_email()
        
        name_field = self.driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div[3]/div/form/input[2]')
        email_field = self.driver.find_element(By.XPATH, "//input[@data-qa='signup-email']")
        
        name_field.clear()
        name_field.send_keys(username)
        email_field.send_keys(email)
        
        # Step 7: Click 'Signup' button
        signup_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form"]/div/div/div[3]/div/form/button'))
            )
        signup_btn.click()

        assert(self.driver.current_url) == f"{self.base_url}/signup"


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
        
        # 17. Click 'Delete Account' button
        delete_account_btn = self.driver.find_element(By.LINK_TEXT, "Delete Account")
        delete_account_btn.click()
        
        # 18. Verify 'ACCOUNT DELETED!' is visible
        account_deleted_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[@data-qa='account-deleted']")))
        assert account_deleted_text.is_displayed()
        
        continue_btn = self.driver.find_element(By.XPATH, "//a[@data-qa='continue-button']")
        continue_btn.click()
