import pytest
import allure
from utils.__allure_helpers import step
from sources.api.dummyjson.auth_client import AuthClient


@pytest.mark.api
@pytest.mark.regression
@allure.epic("DummyJSON API")
@allure.feature("Authentication")
@allure.story("Auth API Endpoints")
class TestDummyAuthAPI:
    @allure.id("DMJS-AUTH-200-001")
    @allure.title("DMJS-AUTH-200-001 - Login Success")
    async def test_login_success(self, auth_client: AuthClient):
        username = "emilys"
        password = "emilyspass"

        with step("Login with valid credentials"):
            response = await auth_client.login(username=username, password=password)

        with step("Verify login response"):
            assert response.status_code == 200
            data = response.json()
            assert "accessToken" in data
            assert "refreshToken" in data
            assert "id" in data
            assert "username" in data
            assert "email" in data

        with step("Verify token format"):
            assert len(data["accessToken"].split(".")) == 3
            assert len(data["refreshToken"].split(".")) == 3

    @allure.id("DMJS-AUTH-400-001")
    @allure.title("DMJS-AUTH-400-001 - Login with Invalid Credentials")
    async def test_login_invalid_credentials(self, auth_client: AuthClient):
        with step("Attempt login with invalid credentials"):
            response = await auth_client.login(
                username="invalid_user",
                password="wrong_password"
            )

        with step("Verify error response"):
            assert response.status_code == 400
            data = response.json()
            assert "message" in data

    @allure.id("DMJS-AUTH-400-002")
    @allure.title("DMJS-AUTH-400-002 - Login with Missing Password")
    async def test_login_missing_password(self, auth_client: AuthClient):
        with step("Attempt login without password"):
            response = await auth_client.login(username="emilys", password="")

        with step("Verify error response"):
            assert response.status_code == 400

    @allure.id("DMJS-AUTH-200-002")
    @allure.title("DMJS-AUTH-200-002 - Get Current Authenticated User")
    async def test_get_current_user(self, auth_client: AuthClient):
        username = "emilys"
        password = "emilyspass"

        with step("Login to get access token"):
            login_response = await auth_client.login(username=username, password=password)
            access_token = login_response.json()["accessToken"]

        with step("Get current user with access token"):
            response = await auth_client.get_current_user(access_token)

        with step("Verify current user data"):
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == username
            assert "id" in data
            assert "email" in data

    @allure.id("DMJS-AUTH-401-001")
    @allure.title("DMJS-AUTH-401-001 - Get Current User with Invalid Token")
    async def test_get_current_user_invalid_token(self, auth_client: AuthClient):
        with step("Attempt to get user with invalid token"):
            response = await auth_client.get_current_user("invalid_token")

        with step("Verify unauthorized response"):
            assert response.status_code == 401
            data = response.json()
            assert "message" in data


    @allure.id("DMJS-AUTH-200-003")
    @allure.title("DMJS-AUTH-200-003 - Refresh Access Token")
    async def test_refresh_token_success(self, auth_client: AuthClient):
        username = "emilys"
        password = "emilyspass"

        with step("Login to get refresh token"):
            login_response = await auth_client.login(username=username, password=password)
            refresh_token = login_response.json()["refreshToken"]

        with step("Refresh access token"):
            response = await auth_client.refresh_token(refresh_token)

        with step("Verify new tokens"):
            assert response.status_code == 200
            data = response.json()
            assert "accessToken" in data
            assert "refreshToken" in data


    @allure.id("DMJS-AUTH-403-001")
    @allure.title("DMJS-AUTH-403-001 - Refresh Token with Invalid Token")
    async def test_refresh_token_invalid(self, auth_client: AuthClient):
        with step("Attempt to refresh with invalid token"):
            response = await auth_client.refresh_token("invalid_refresh_token")

        with step("Verify forbidden response"):
            assert response.status_code == 403


    @allure.id("DMJS-AUTH-200-004")
    @allure.title("DMJS-AUTH-200-004 - Login with Custom Expiration")
    async def test_login_custom_expiration(self, auth_client: AuthClient):
        username = "emilys"
        password = "emilyspass"

        with step("Login with 60 minute expiration"):
            response = await auth_client.login(
                username=username,
                password=password,
                expires_in_mins=60
            )

        with step("Verify login successful"):
            assert response.status_code == 200
            data = response.json()
            assert "accessToken" in data
            assert "refreshToken" in data


    @allure.id("DMJS-AUTH-200-005")
    @allure.title("DMJS-AUTH-200-005 - Complete Auth Flow")
    async def test_complete_auth_flow(self, auth_client: AuthClient):
        username = "emilys"
        password = "emilyspass"

        with step("Step 1: Login"):
            login_response = await auth_client.login(username=username, password=password)
            login_data = login_response.json()
            access_token = login_data["accessToken"]
            refresh_token = login_data["refreshToken"]

        with step("Step 2: Use access token to get current user"):
            user_response = await auth_client.get_current_user(access_token)
            assert user_response.status_code == 200

        with step("Step 3: Refresh the access token"):
            refresh_response = await auth_client.refresh_token(refresh_token)
            assert refresh_response.status_code == 200
            new_access_token = refresh_response.json()["accessToken"]

        with step("Step 4: Use new access token"):
            final_response = await auth_client.get_current_user(new_access_token)
            assert final_response.status_code == 200
