from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.login_signup_page import LoginSignupPage
from .base_page import BasePage


class HomePage(BasePage):
    
    def goto_signup_login(self):
        self.driver.get(self.base_url)
        assert "Automation Exercise" in self.driver.title
        
        # Click on 'Signup / Login' button
        signup_login_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Signup / Login")))
        signup_login_btn.click()
        
        # Verify 'New User Signup!' is visible
        signup_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'New User Signup!')]")))
        assert signup_text.is_displayed()
    
    def delete_account(self):
        LoginSignupPage.signup(self)
        # Click 'Delete Account' button
        delete_account_btn = self.driver.find_element(By.LINK_TEXT, "Delete Account")
        delete_account_btn.click()
        
        # Verify 'ACCOUNT DELETED!' is visible
        account_deleted_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[@data-qa='account-deleted']")))
        assert account_deleted_text.is_displayed()
        
        continue_btn = self.driver.find_element(By.XPATH, "//a[@data-qa='continue-button']")
        continue_btn.click()

    def logout(self):
        LoginSignupPage.login(self)
        # Click on 'Logout' button
        logout_btn = self.driver.find_element(By.LINK_TEXT, "Logout")
        logout_btn.click()
        
        # Verify 'Logged out successfully' message is displayed
        logged_out_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Logged out successfully')]")))
        assert logged_out_text.is_displayed()
        
        # Verify user is redirected to home page
        assert self.driver.current_url == f"{self.base_url}/"