import requests
import pytest
import json
import time
from urllib.parse import urljoin
# from typing import Dict, Any, Optional

class AmwayAPITester:
    """API Testing framework for Amway Taiwan website"""
    
    def __init__(self, base_url: str = "https://shop.amway.com.tw/sit"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/json'
        })
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.request(method, url, timeout=30, **kwargs)
            print(f"Request to {url} completed with status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response body: {response.text[:100]}...")  # Print first 100 chars of body
            print(f"Request method: {method}, Endpoint: {endpoint}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
    
    def test_homepage_api(self):
        """Test homepage API endpoints"""
        print("Testing Homepage API...")
        
        # Test main page load
        response = self.make_request('GET', '/')
        assert response.status_code == 200, f"Homepage failed: {response.status_code}"
        print("✓ Homepage loads successfully")
        
        # Test common API endpoints that might exist
        common_endpoints = [
            '/api/products',
            '/api/categories',
            '/api/user/profile',
            '/api/cart',
            '/api/config'
        ]
        
        for endpoint in common_endpoints:
            try:
                response = self.make_request('GET', endpoint)
                if response.status_code == 200:
                    print(f"✓ {endpoint} - Status: {response.status_code}")
                elif response.status_code == 401:
                    print(f"○ {endpoint} - Requires authentication")
                else:
                    print(f"△ {endpoint} - Status: {response.status_code}")
            except Exception as e:
                print(f"✗ {endpoint} - Error: {str(e)}")
    
    def test_product_search_api(self, search_term: str = "維他命"):
        """Test product search functionality"""
        print(f"Testing Product Search API with term: '{search_term}'...")
        
        # Test search endpoints
        search_endpoints = [
            f'/api/search?q={search_term}',
            f'/api/products/search?keyword={search_term}',
            f'/search?query={search_term}'
        ]
        
        for endpoint in search_endpoints:
            try:
                response = self.make_request('GET', endpoint)
                if response.status_code == 200:
                    print(f"✓ Search endpoint {endpoint} - Status: {response.status_code}")
                    try:
                        data = response.json()
                        if isinstance(data, dict) and 'results' in data:
                            print(f"  Found {len(data.get('results', []))} results")
                    except json.JSONDecodeError:
                        print("  Response is not JSON format")
                else:
                    print(f"△ Search endpoint {endpoint} - Status: {response.status_code}")
            except Exception as e:
                print(f"✗ Search endpoint {endpoint} - Error: {str(e)}")
    
    def test_authentication_apis(self):
        """Test authentication related APIs"""
        print("Testing Authentication APIs...")
        
        auth_endpoints = [
            ('/api/auth/login', 'POST'),
            ('/api/user/login', 'POST'),
            ('/login', 'POST'),
            ('/api/auth/register', 'POST'),
            ('/api/user/register', 'POST')
        ]
        
        test_credentials = {
            "username": "test@example.com",
            "password": "testpassword123",
            "email": "test@example.com"
        }
        
        for endpoint, method in auth_endpoints:
            try:
                response = self.make_request(method, endpoint, json=test_credentials)
                if response.status_code in [200, 400, 401, 422]:
                    print(f"✓ {method} {endpoint} - Status: {response.status_code}")
                    if response.status_code == 400:
                        print("  (Expected - invalid test credentials)")
                else:
                    print(f"△ {method} {endpoint} - Unexpected status: {response.status_code}")
            except Exception as e:
                print(f"✗ {method} {endpoint} - Error: {str(e)}")
    
    def test_cart_apis(self):
        """Test shopping cart APIs"""
        print("Testing Shopping Cart APIs...")
        
        cart_endpoints = [
            ('/api/cart', 'GET'),
            ('/api/cart/items', 'GET'),
            ('/api/cart/add', 'POST'),
            ('/api/cart/update', 'PUT'),
            ('/api/cart/remove', 'DELETE')
        ]
        
        test_item = {
            "productId": "12345",
            "quantity": 1,
            "variant": "default"
        }
        
        for endpoint, method in cart_endpoints:
            try:
                if method == 'GET':
                    response = self.make_request(method, endpoint)
                else:
                    response = self.make_request(method, endpoint, json=test_item)
                
                if response.status_code in [200, 401, 404]:
                    print(f"✓ {method} {endpoint} - Status: {response.status_code}")
                    if response.status_code == 401:
                        print("  (Requires authentication)")
                else:
                    print(f"△ {method} {endpoint} - Status: {response.status_code}")
            except Exception as e:
                print(f"✗ {method} {endpoint} - Error: {str(e)}")
    
    def test_performance(self, endpoint: str = '/'):
        """Test API performance"""
        print(f"Testing Performance for {endpoint}...")
        
        response_times = []
        for i in range(5):
            start_time = time.time()
            try:
                response = self.make_request('GET', endpoint)
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # Convert to ms
                response_times.append(response_time)
                print(f"  Request {i+1}: {response_time:.2f}ms - Status: {response.status_code}")
            except Exception as e:
                print(f"  Request {i+1}: Failed - {str(e)}")
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            print(f"Average response time: {avg_time:.2f}ms")
            
            if avg_time < 1000:
                print("✓ Performance: Good (< 1 second)")
            elif avg_time < 3000:
                print("○ Performance: Acceptable (1-3 seconds)")
            else:
                print("△ Performance: Slow (> 3 seconds)")
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("Testing Error Handling...")
        
        # Test invalid endpoints
        invalid_endpoints = [
            '/api/nonexistent',
            '/invalid/path',
            '/api/products/99999999'
        ]
        
        for endpoint in invalid_endpoints:
            try:
                response = self.make_request('GET', endpoint)
                if response.status_code == 404:
                    print(f"✓ {endpoint} - Correctly returns 404")
                else:
                    print(f"△ {endpoint} - Status: {response.status_code}")
            except Exception as e:
                print(f"✗ {endpoint} - Error: {str(e)}")
        
        # Test malformed requests
        try:
            response = self.make_request('POST', '/api/test', json={"invalid": "json"})
            print(f"✓ Malformed request handled - Status: {response.status_code}")
        except Exception as e:
            print(f"✗ Malformed request test failed: {str(e)}")
    
    def run_all_tests(self):
        """Run comprehensive API test suite"""
        print("=" * 60)
        print("AMWAY TAIWAN API TEST SUITE")
        print("=" * 60)
        print(f"Base URL: {self.base_url}")
        print("=" * 60)
        
        try:
            self.test_homepage_api()
            print("\n" + "-" * 40)
            
            self.test_product_search_api()
            print("\n" + "-" * 40)
            
            self.test_authentication_apis()
            print("\n" + "-" * 40)
            
            self.test_cart_apis()
            print("\n" + "-" * 40)
            
            self.test_performance()
            print("\n" + "-" * 40)
            
            self.test_error_handling()
            print("\n" + "=" * 60)
            print("API TESTING COMPLETED")
            print("=" * 60)
            
        except Exception as e:
            print(f"Test suite failed: {str(e)}")

# Pytest test cases for automated testing
class TestAmwayAPI:
    """Pytest test cases for Amway API"""
    
    @classmethod
    def setup_class(cls):
        cls.api_tester = AmwayAPITester()
    
    def test_homepage_availability(self):
        """Test if homepage is accessible"""
        response = self.api_tester.make_request('GET', '/')
        assert response.status_code == 200
    
    def test_response_headers(self):
        """Test response headers"""
        response = self.api_tester.make_request('GET', '/')
        assert 'content-type' in response.headers
    
    def test_response_time(self):
        """Test response time is reasonable"""
        start_time = time.time()
        response = self.api_tester.make_request('GET', '/')
        end_time = time.time()
        response_time = end_time - start_time
        assert response_time < 10, f"Response time too slow: {response_time}s"
    
    @pytest.mark.parametrize("endpoint", [
        '/api/products',
        '/api/categories',
        '/api/config'
    ])
    def test_common_endpoints(self, endpoint):
        """Test common API endpoints"""
        response = self.api_tester.make_request('GET', endpoint)
        # Accept various status codes as they might require auth
        assert response.status_code in [200, 401, 404]

# Usage example
if __name__ == "__main__":
    # Create and run the test suite
    tester = AmwayAPITester()
    tester.run_all_tests()
    
    print("\n" + "=" * 60)
    print("To run pytest tests, use:")
    print("pytest test_amway_api.py -v")
    print("=" * 60)