import pytest
import allure
from utils.__allure_helpers import step
from sources.api.dummyjson.auth_client import AuthClient


@pytest.mark.api
@pytest.mark.regression
@allure.epic("DummyJSON API")
@allure.feature("Authentication")
@allure.story("Negative Cases")
class TestAuthNegative:
    @allure.id("DMJS-AUTH-400-001")
    @allure.title("DMJS-AUTH-400-001 - Login with Invalid Credentials")
    async def test_login_invalid_credentials(self, auth_client: AuthClient):
        with step("Attempt login with invalid credentials"):
            response = await auth_client.login(
                username="invalid_user",
                password="wrong_password")

        with step("Verify error response"):
            assert response.status_code == 400
            assert isinstance(response.json(), dict)
            
        with step("Verify error message content"):
            data = response.json()
            assert "message" in data
            assert isinstance(data["message"], str), "Message should be a string"
            assert data["message"] == "Invalid credentials"

    @allure.id("DMJS-AUTH-400-002")
    @allure.title("DMJS-AUTH-400-002 - Login with Missing Password")
    async def test_login_missing_password(self, auth_client: AuthClient):
        with step("Attempt login without password"):
            response = await auth_client.login(username="emilys", password="")

        with step("Verify error response"):
            assert response.status_code == 400
            assert isinstance(response.json(), dict)
        
        with step("Verify error message content"):
            data = response.json()
            assert "message" in data
            assert isinstance(data["message"], str), "Message should be a string"
            assert data["message"] == "Username and password required"

    @allure.id("DMJS-AUTH-400-003")
    @allure.title("DMJS-AUTH-400-003 - Login with Empty Username")
    async def test_login_empty_username(self, auth_client: AuthClient):
        with step("Attempt login with empty username"):
            response = await auth_client.login(username="", password="emilyspass")

        with step("Verify error response"):
            assert response.status_code == 400
            assert isinstance(response.json(), dict)
        
        with step("Verify error message content"):
            data = response.json()
            assert "message" in data
            assert isinstance(data["message"], str), "Message should be a string"
            assert data["message"] == "Username and password required"

    @allure.id("DMJS-AUTH-400-004")
    @allure.title("DMJS-AUTH-400-004 - Login with Non-existent User")
    async def test_login_nonexistent_user(self, auth_client: AuthClient):
        with step("Attempt login with non-existent user"):
            response = await auth_client.login(username="nonexistent_user_12345", password="anypassword")

        with step("Verify error response"):
            assert response.status_code == 400
            assert isinstance(response.json(), dict)
            
        with step("Verify error message content"):
            data = response.json()
            assert "message" in data
            assert isinstance(data["message"], str), "Message should be a string"
            assert data["message"] == "Invalid credentials"

    @allure.id("DMJS-AUTH-400-005")
    @allure.title("DMJS-AUTH-400-005 - Login with Wrong Password")
    async def test_login_wrong_password(self, auth_client: AuthClient):
        with step("Attempt login with wrong password"):
            response = await auth_client.login(
                username="emilys", 
                password="wrongpassword123")

        with step("Verify error response"):
            assert response.status_code == 400
            assert isinstance(response.json(), dict)
            
        with step("Verify error message content"):
            data = response.json()
            assert "message" in data
            assert isinstance(data["message"], str), "Message should be a string"
            assert data["message"] == "Invalid credentials"

    @allure.id("DMJS-AUTH-401-001")
    @allure.title("DMJS-AUTH-401-001 - Get Current User with Invalid Token")
    async def test_get_current_user_invalid_token(self, auth_client: AuthClient):
        with step("Attempt to get user with invalid token"):
            response = await auth_client.get_current_user("invalid_token")
        
        with step("Verify unauthorized response"):
            assert response.status_code == 401
            assert isinstance(response.json(), dict)
            
        with step("Verify error message content"):
            data = response.json()
            assert "message" in data
            assert isinstance(data["message"], str)
            assert data["message"] == "Invalid/Expired Token!"

    @allure.id("DMJS-AUTH-401-002")
    @allure.title("DMJS-AUTH-401-002 - Get Current User with Malformed Token")
    async def test_get_current_user_malformed_token(self, auth_client: AuthClient):
        with step("Attempt to get user with malformed token"):
            response = await auth_client.get_current_user("not.a.valid.jwt.token.format")

        with step("Verify unauthorized response"):
            assert response.status_code == 401
            assert isinstance(response.json(), dict)
            
        with step("Verify error message content"):
            data = response.json()
            assert "message" in data
            assert isinstance(data["message"], str)
            assert data["message"] == "Invalid/Expired Token!"
            
    @allure.id("DMJS-AUTH-401-003")
    @allure.title("DMJS-AUTH-401-003 - Refresh Token with Empty Token")
    async def test_refresh_token_empty(self, auth_client: AuthClient):
        with step("Attempt to refresh with empty token"):
            response = await auth_client.refresh_token("")

        with step("Verify error response"):
            assert response.status_code == 401
            assert isinstance(response.json(), dict)
            
        with step("Verify error message content"):
            data = response.json()
            assert "message" in data
            assert isinstance(data["message"], str)
            assert data["message"] == "Refresh token required"

    @allure.id("DMJS-AUTH-403-001")
    @allure.title("DMJS-AUTH-403-001 - Refresh Token with Invalid Token")
    async def test_refresh_token_invalid(self, auth_client: AuthClient):
        with step("Attempt to refresh with invalid token"):
            response = await auth_client.refresh_token("invalid_refresh_token")

        with step("Verify forbidden response"):
            assert response.status_code == 403
            assert isinstance(response.json(), dict)
            
        with step("Verify error message content"):
            data = response.json()
            assert "message" in data
            assert isinstance(data["message"], str)
            assert data["message"] == "Invalid refresh token"


