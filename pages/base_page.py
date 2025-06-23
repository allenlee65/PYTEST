from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import random
import string
import pytest


class BasePage:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method to initialize WebDriver before each test"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
        chrome_options.add_experimental_option("prefs", { "profile.default_content_setting_values.geolocation": 2})
        ##chrome_options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://automationexercise.com"
        self.DOWNLOAD_DIR = "D:\\_Downloads"
        yield
        # Teardown
        self.driver.quit()

    def generate_random_email(self):
        """Generate random email for testing"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_string}@example.com"

    def generate_random_name(self):
        """Generate random name for testing"""
        names = ["John", "Jane", "Mike", "Sarah", "David", "Emma", "Alex", "Lisa"]
        return random.choice(names) + str(random.randint(100, 999))
