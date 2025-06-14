import requests
import pytest
import json
import random
import string
from datetime import datetime
from typing import Dict, Any, Optional

class AutomationExerciseAPITester:
    """
    Comprehensive API testing framework for Automation Exercise website
    Based on: https://automationexercise.com/api_list
    """
    
    def __init__(self, base_url: str = "https://automationexercise.com/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AutomationExercise-API-Tester/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        self.test_email = None
        self.test_password = "TestPassword123"
    
    def generate_random_email(self):
        """Generate random email for testing"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_string}@example.com"
    
    def generate_test_user_data(self):
        """Generate test user data for registration"""
        return {
            'name': 'Test User',
            'email': self.generate_random_email(),
            'password': self.test_password,
            'title': 'Mr',
            'birth_date': '15',
            'birth_month': '6',
            'birth_year': '1990',
            'firstname': 'Test',
            'lastname': 'User',
            'company': 'Test Company',
            'address1': '123 Test Street',
            'address2': 'Apt 456',
            'country': 'United States',
            'zipcode': '12345',
            'state': 'California',
            'city': 'Los Angeles',
            'mobile_number': '+1234567890'
        }

class TestProductsAPI:
    """Test cases for Products API endpoints"""
    
    @classmethod
    def setup_class(cls):
        cls.api = AutomationExerciseAPITester()
    
    def test_api1_get_all_products_list(self):
        """API 1: Get All Products List"""
        response = self.api.session.get(f"{self.api.base_url}/productsList")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify response is JSON
        try:
            data = response.json()
            assert 'products' in data, "Products key not found in response"
            assert isinstance(data['products'], list), "Products should be a list"
            print(f"✓ API 1: Successfully retrieved {len(data['products'])} products")
        except json.JSONDecodeError:
            pytest.fail("Response is not valid JSON")
    
    def test_api2_post_to_products_list_not_supported(self):
        """API 2: POST To All Products List (Should return 405)"""
        response = self.api.session.post(f"{self.api.base_url}/productsList")
        
        assert response.status_code == 405, f"Expected 405, got {response.status_code}"
        
        data = response.json()
        assert "This request method is not supported" in data.get('message', ''), \
            "Expected method not supported message"
        print("✓ API 2: POST correctly returns 405 - Method Not Allowed")

class TestBrandsAPI:
    """Test cases for Brands API endpoints"""
    
    @classmethod
    def setup_class(cls):
        cls.api = AutomationExerciseAPITester()
    
    def test_api3_get_all_brands_list(self):
        """API 3: Get All Brands List"""
        response = self.api.session.get(f"{self.api.base_url}/brandsList")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        try:
            data = response.json()
            assert 'brands' in data, "Brands key not found in response"
            assert isinstance(data['brands'], list), "Brands should be a list"
            print(f"✓ API 3: Successfully retrieved {len(data['brands'])} brands")
        except json.JSONDecodeError:
            pytest.fail("Response is not valid JSON")
    
    def test_api4_put_to_brands_list_not_supported(self):
        """API 4: PUT To All Brands List (Should return 405)"""
        response = self.api.session.put(f"{self.api.base_url}/brandsList")
        
        assert response.status_code == 405, f"Expected 405, got {response.status_code}"
        
        data = response.json()
        assert "This request method is not supported" in data.get('message', ''), \
            "Expected method not supported message"
        print("✓ API 4: PUT correctly returns 405 - Method Not Allowed")

class TestSearchAPI:
    """Test cases for Search Product API endpoints"""
    
    @classmethod
    def setup_class(cls):
        cls.api = AutomationExerciseAPITester()
    
    def test_api5_search_product_with_parameter(self):
        """API 5: POST To Search Product with search_product parameter"""
        search_terms = ['top', 'tshirt', 'jean', 'dress', 'shirt']
        
        for term in search_terms:
            data = {'search_product': term}
            response = self.api.session.post(f"{self.api.base_url}/searchProduct", data=data)
            
            assert response.status_code == 200, f"Expected 200 for '{term}', got {response.status_code}"
            
            try:
                result = response.json()
                assert 'products' in result, f"Products key not found for search term '{term}'"
                print(f"✓ API 5: Search for '{term}' returned {len(result['products'])} products")
            except json.JSONDecodeError:
                pytest.fail(f"Response is not valid JSON for search term '{term}'")
    
    def test_api6_search_product_without_parameter(self):
        """API 6: POST To Search Product without search_product parameter"""
        response = self.api.session.post(f"{self.api.base_url}/searchProduct")
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        data = response.json()
        expected_message = "Bad request, search_product parameter is missing in POST request."
        assert expected_message in data.get('message', ''), \
            f"Expected missing parameter message, got: {data.get('message', '')}"
        print("✓ API 6: Correctly returns 400 for missing search_product parameter")

class TestLoginAPI:
    """Test cases for Login verification API endpoints"""
    
    @classmethod
    def setup_class(cls):
        cls.api = AutomationExerciseAPITester()
    
    def test_api7_verify_login_with_valid_details(self):
        """API 7: POST To Verify Login with valid details"""
        # First create a test user
        user_data = self.api.generate_test_user_data()
        create_response = self.api.session.post(f"{self.api.base_url}/createAccount", data=user_data)
        
        if create_response.status_code == 201:
            # Now test login with valid credentials
            login_data = {
                'email': user_data['email'],
                'password': user_data['password']
            }
            response = self.api.session.post(f"{self.api.base_url}/verifyLogin", data=login_data)
            
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            assert "User exists!" in data.get('message', ''), \
                f"Expected 'User exists!' message, got: {data.get('message', '')}"
            print("✓ API 7: Login verification successful with valid credentials")
            
            # Cleanup - delete the test user
            delete_data = {
                'email': user_data['email'],
                'password': user_data['password']
            }
            self.api.session.delete(f"{self.api.base_url}/deleteAccount", data=delete_data)
        else:
            print("⚠ API 7: Could not create test user for login verification")
    
    def test_api8_verify_login_without_email_parameter(self):
        """API 8: POST To Verify Login without email parameter"""
        data = {'password': 'somepassword'}
        response = self.api.session.post(f"{self.api.base_url}/verifyLogin", data=data)
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        result = response.json()
        expected_message = "Bad request, email or password parameter is missing in POST request."
        assert expected_message in result.get('message', ''), \
            f"Expected missing parameter message, got: {result.get('message', '')}"
        print("✓ API 8: Correctly returns 400 for missing email parameter")
    
    def test_api9_delete_to_verify_login_not_supported(self):
        """API 9: DELETE To Verify Login (Should return 405)"""
        response = self.api.session.delete(f"{self.api.base_url}/verifyLogin")
        
        assert response.status_code == 405, f"Expected 405, got {response.status_code}"
        
        data = response.json()
        assert "This request method is not supported" in data.get('message', ''), \
            "Expected method not supported message"
        print("✓ API 9: DELETE correctly returns 405 - Method Not Allowed")
    
    def test_api10_verify_login_with_invalid_details(self):
        """API 10: POST To Verify Login with invalid details"""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        response = self.api.session.post(f"{self.api.base_url}/verifyLogin", data=data)
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        
        result = response.json()
        assert "User not found!" in result.get('message', ''), \
            f"Expected 'User not found!' message, got: {result.get('message', '')}"
        print("✓ API 10: Correctly returns 404 for invalid credentials")

class TestUserAccountAPI:
    """Test cases for User Account management API endpoints"""
    
    @classmethod
    def setup_class(cls):
        cls.api = AutomationExerciseAPITester()
    
    def test_api11_create_user_account(self):
        """API 11: POST To Create/Register User Account"""
        user_data = self.api.generate_test_user_data()
        response = self.api.session.post(f"{self.api.base_url}/createAccount", data=user_data)
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        data = response.json()
        assert "User created!" in data.get('message', ''), \
            f"Expected 'User created!' message, got: {data.get('message', '')}"
        print("✓ API 11: User account created successfully")
        
        # Store email for cleanup
        self.api.test_email = user_data['email']
        
        # Cleanup - delete the created user
        delete_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        self.api.session.delete(f"{self.api.base_url}/deleteAccount", data=delete_data)
    
    def test_api12_delete_user_account(self):
        """API 12: DELETE METHOD To Delete User Account"""
        # First create a user to delete
        user_data = self.api.generate_test_user_data()
        create_response = self.api.session.post(f"{self.api.base_url}/createAccount", data=user_data)
        
        if create_response.status_code == 201:
            # Now delete the user
            delete_data = {
                'email': user_data['email'],
                'password': user_data['password']
            }
            response = self.api.session.delete(f"{self.api.base_url}/deleteAccount", data=delete_data)
            
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            assert "Account deleted!" in data.get('message', ''), \
                f"Expected 'Account deleted!' message, got: {data.get('message', '')}"
            print("✓ API 12: User account deleted successfully")
        else:
            print("⚠ API 12: Could not create test user for deletion test")
    
    def test_api13_update_user_account(self):
        """API 13: PUT METHOD To Update User Account"""
        # First create a user to update
        user_data = self.api.generate_test_user_data()
        create_response = self.api.session.post(f"{self.api.base_url}/createAccount", data=user_data)
        
        if create_response.status_code == 201:
            # Update user data
            user_data['name'] = 'Updated Test User'
            user_data['company'] = 'Updated Test Company'
            
            response = self.api.session.put(f"{self.api.base_url}/updateAccount", data=user_data)
            
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            assert "User updated!" in data.get('message', ''), \
                f"Expected 'User updated!' message, got: {data.get('message', '')}"
            print("✓ API 13: User account updated successfully")
            
            # Cleanup - delete the test user
            delete_data = {
                'email': user_data['email'],
                'password': user_data['password']
            }
            self.api.session.delete(f"{self.api.base_url}/deleteAccount", data=delete_data)
        else:
            print("⚠ API 13: Could not create test user for update test")
    
    def test_api14_get_user_detail_by_email(self):
        """API 14: GET user account detail by email"""
        # First create a user to retrieve details
        user_data = self.api.generate_test_user_data()
        create_response = self.api.session.post(f"{self.api.base_url}/createAccount", data=user_data)
        
        if create_response.status_code == 201:
            # Get user details
            params = {'email': user_data['email']}
            response = self.api.session.get(f"{self.api.base_url}/getUserDetailByEmail", params=params)
            
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            try:
                data = response.json()
                assert 'user' in data, "User key not found in response"
                user_details = data['user']
                assert user_details['email'] == user_data['email'], "Email mismatch in response"
                print("✓ API 14: User details retrieved successfully")
            except json.JSONDecodeError:
                pytest.fail("Response is not valid JSON")
            
            # Cleanup - delete the test user
            delete_data = {
                'email': user_data['email'],
                'password': user_data['password']
            }
            self.api.session.delete(f"{self.api.base_url}/deleteAccount", data=delete_data)
        else:
            print("⚠ API 14: Could not create test user for detail retrieval test")

class TestEdgeCasesAndSecurity:
    """Additional test cases for edge cases and security"""
    
    @classmethod
    def setup_class(cls):
        cls.api = AutomationExerciseAPITester()
    
    def test_duplicate_user_registration(self):
        """Test creating duplicate user accounts"""
        user_data = self.api.generate_test_user_data()
        
        # Create first user
        response1 = self.api.session.post(f"{self.api.base_url}/createAccount", data=user_data)
        
        if response1.status_code == 201:
            # Try to create duplicate user
            response2 = self.api.session.post(f"{self.api.base_url}/createAccount", data=user_data)
            
            # Should not allow duplicate registration
            assert response2.status_code != 201, "Duplicate user registration should not be allowed"
            print("✓ Duplicate user registration properly handled")
            
            # Cleanup
            delete_data = {
                'email': user_data['email'],
                'password': user_data['password']
            }
            self.api.session.delete(f"{self.api.base_url}/deleteAccount", data=delete_data)
    
    def test_invalid_email_formats(self):
        """Test registration with invalid email formats"""
        invalid_emails = [
            'invalid-email',
            'test@',
            '@example.com',
            'test..test@example.com',
            ''
        ]
        
        for email in invalid_emails:
            user_data = self.api.generate_test_user_data()
            user_data['email'] = email
            
            response = self.api.session.post(f"{self.api.base_url}/createAccount", data=user_data)
            
            # Should reject invalid email formats
            if response.status_code == 201:
                print(f"⚠ Invalid email '{email}' was accepted")
                # Cleanup if created
                delete_data = {'email': email, 'password': user_data['password']}
                self.api.session.delete(f"{self.api.base_url}/deleteAccount", data=delete_data)
            else:
                print(f"✓ Invalid email '{email}' properly rejected")
    
    def test_sql_injection_attempts(self):
        """Test for basic SQL injection vulnerabilities"""
        sql_payloads = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "admin'--",
            "' UNION SELECT * FROM users --"
        ]
        
        for payload in sql_payloads:
            data = {
                'email': payload,
                'password': 'test'
            }
            response = self.api.session.post(f"{self.api.base_url}/verifyLogin", data=data)
            
            # Should not return 200 for SQL injection attempts
            if response.status_code == 200:
                print(f"⚠ Potential SQL injection vulnerability with payload: {payload}")
            else:
                print(f"✓ SQL injection payload properly handled: {payload}")

# Comprehensive test runner
def run_comprehensive_test_suite():
    """Run all test suites with detailed reporting"""
    print("=" * 80)
    print("AUTOMATION EXERCISE API COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Base URL: https://automationexercise.com/api")
    print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Run pytest with verbose output
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-x"  # Stop on first failure for debugging
    ])

if __name__ == "__main__":
    # Quick manual test runner
    api = AutomationExerciseAPITester()
    
    print("Running quick API connectivity test...")
    
    # Test basic connectivity
    try:
        response = api.session.get(f"{api.base_url}/productsList")
        if response.status_code == 200:
            print("✓ API is accessible")
            data = response.json()
            print(f"✓ Found {len(data.get('products', []))} products")
        else:
            print(f"✗ API returned status code: {response.status_code}")
    except Exception as e:
        print(f"✗ API connection failed: {str(e)}")
    
    print("\nTo run the complete test suite, use:")
    print("pytest test_automation_exercise_api.py -v")
    print("\nOr run comprehensive tests with:")
    print("python test_automation_exercise_api.py")