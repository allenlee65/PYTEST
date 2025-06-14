import httpx
import pytest
from pytest_httpx import HTTPXMock

@pytest.fixture
def mock_httpx_response(httpx_mock: HTTPXMock):
    # 使用 httpx_mock 來攔截請求，並模擬回應
    httpx_mock.add_response(
        url="https://api.example.com/data",  # 指定要攔截的 API URL
        json={"message": "success"}, # 模擬 API 回傳的 JSON 資料
        status_code=200  # 設定 HTTP 狀態碼為 200（成功）
    )

def test_api(mock_httpx_response: None):
    # 這裡的 httpx.get() 不會真的發送 HTTP 請求，而是直接回傳模擬的回應
    response = httpx.get("https://api.example.com/data")
    
    # 驗證回應的狀態碼是否正確
    assert response.status_code == 200

    # 驗證回應的 JSON 內容是否正確
    assert response.json() == {"message": "success"}

# @pytest.fixture
# def mock_404_response(httpx_mock):
#     httpx_mock.add_response(
#         url="https://api.example.com/notfound",
#         status_code=404,
#         json={"error": "Not Found"}
#     )

# def test_api_404(mock_404_response):
#     response = httpx.get("https://api.example.com/notfound")
#     assert response.status_code == 404
#     assert response.json() == {"error": "Not Found"}

# @pytest.fixture
# def mock_500_response(httpx_mock):
#     httpx_mock.add_response(
#         url="https://api.example.com/server-error",
#         status_code=500,
#         json={"error": "Internal Server Error"}
#     )

# def test_api_500(mock_500_response):
#     response = httpx.get("https://api.example.com/server-error")
#     assert response.status_code == 500
#     assert response.json() == {"error": "Internal Server Error"}