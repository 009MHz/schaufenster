import pytest
import allure
from utils.__allure_helpers import step
from sources.api.dummyjson.auth_client import AuthClient

USER_CREDENTIALS = {
    "username": "emilys",
    "password": "emilyspass"
}


@pytest.mark.api
@pytest.mark.regression
@allure.epic("DummyJSON API")
@allure.feature("Authentication")
@allure.story("Basic Auth Flow")
class TestAuthBasic:
    @allure.id("DMJS-AUTH-200-001")
    @allure.title("DMJS-AUTH-200-001 - Login Success")
    async def test_login_success(self, auth_client: AuthClient):
        username = USER_CREDENTIALS["username"]
        password = USER_CREDENTIALS["password"]

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

    @allure.id("DMJS-AUTH-200-002")
    @allure.title("DMJS-AUTH-200-002 - Get Current Authenticated User")
    async def test_get_current_user(self, auth_client: AuthClient):
        username = USER_CREDENTIALS["username"]
        password = USER_CREDENTIALS["password"]

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

    @allure.id("DMJS-AUTH-200-003")
    @allure.title("DMJS-AUTH-200-003 - Refresh Access Token")
    async def test_refresh_token_success(self, auth_client: AuthClient):
        username = USER_CREDENTIALS["username"]
        password = USER_CREDENTIALS["password"]

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

    @allure.id("DMJS-AUTH-200-004")
    @allure.title("DMJS-AUTH-200-004 - Login with Custom Expiration")
    async def test_login_custom_expiration(self, auth_client: AuthClient):
        username = USER_CREDENTIALS["username"]
        password = USER_CREDENTIALS["password"]

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
        username = USER_CREDENTIALS["username"]
        password = USER_CREDENTIALS["password"]

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


@pytest.mark.api
@pytest.mark.regression
@allure.epic("DummyJSON API")
@allure.feature("Authentication")
@allure.story("Schema Validation")
class TestAuthSchema:
    @allure.id("DMJS-AUTH-200-006")
    @allure.title("DMJS-AUTH-200-006 - Validate Login Response Schema")
    async def test_login_response_schema(self, auth_client: AuthClient):
        username = USER_CREDENTIALS["username"]
        password = USER_CREDENTIALS["password"]

        with step("Login with valid credentials"):
            response = await auth_client.login(username=username, password=password)

        with step("Verify response status"):
            assert response.status_code == 200

        with step("Validate response fields"):
            data = response.json()
            assert "id" in data and isinstance(data["id"], int)
            assert "username" in data and data["username"] == username
            assert "email" in data and "@" in data["email"]
            assert "firstName" in data and len(data["firstName"]) > 0
            assert "lastName" in data and len(data["lastName"]) > 0
            assert "gender" in data
            assert "image" in data
            assert "accessToken" in data and len(data["accessToken"].split(".")) == 3
            assert "refreshToken" in data and len(data["refreshToken"].split(".")) == 3

    @allure.id("DMJS-AUTH-200-007")
    @allure.title("DMJS-AUTH-200-007 - Validate Current User Response Schema")
    async def test_current_user_response_schema(self, auth_client: AuthClient):
        username = USER_CREDENTIALS["username"]
        password = USER_CREDENTIALS["password"]

        with step("Login to get access token"):
            login_response = await auth_client.login(username=username, password=password)
            access_token = login_response.json()["accessToken"]

        with step("Get current user"):
            response = await auth_client.get_current_user(access_token)

        with step("Validate response fields"):
            assert response.status_code == 200
            data = response.json()
            assert "id" in data and isinstance(data["id"], int)
            assert "username" in data and data["username"] == username
            assert "email" in data and "@" in data["email"]
            assert "firstName" in data
            assert "lastName" in data
            assert "gender" in data
            assert "image" in data

    @allure.id("DMJS-AUTH-200-008")
    @allure.title("DMJS-AUTH-200-008 - Validate Refresh Token Response Schema")
    async def test_refresh_token_response_schema(self, auth_client: AuthClient):
        username = USER_CREDENTIALS["username"]
        password = USER_CREDENTIALS["password"]

        with step("Login to get refresh token"):
            login_response = await auth_client.login(username=username, password=password)
            refresh_token = login_response.json()["refreshToken"]

        with step("Refresh access token"):
            response = await auth_client.refresh_token(refresh_token)

        with step("Validate response fields"):
            assert response.status_code == 200
            data = response.json()
            assert "accessToken" in data and len(data["accessToken"].split(".")) == 3
            assert "refreshToken" in data and len(data["refreshToken"].split(".")) == 3


@pytest.mark.api
@pytest.mark.regression
@allure.epic("DummyJSON API")
@allure.feature("Authentication")
@allure.story("Functional Tests")
class TestAuthFunctionality:
    @allure.id("DMJS-AUTH-200-009")
    @allure.title("DMJS-AUTH-200-009 - Token Refresh Flow")
    async def test_token_refresh_flow(self, auth_client: AuthClient):
        username = USER_CREDENTIALS["username"]
        password = USER_CREDENTIALS["password"]

        with step("Login to get refresh token"):
            login_response = await auth_client.login(username=username, password=password)
            refresh_token = login_response.json()["refreshToken"]

        with step("Refresh access token"):
            refresh_response = await auth_client.refresh_token(refresh_token)
            assert refresh_response.status_code == 200
            new_access_token = refresh_response.json()["accessToken"]

        with step("Verify new access token works"):
            user_response = await auth_client.get_current_user(new_access_token)
            assert user_response.status_code == 200

    @allure.id("DMJS-AUTH-200-010")
    @allure.title("DMJS-AUTH-200-010 - Username Case Sensitivity")
    async def test_username_case_sensitivity(self, auth_client: AuthClient):
        username = USER_CREDENTIALS["username"]
        password = USER_CREDENTIALS["password"]

        with step("Login with lowercase username"):
            response1 = await auth_client.login(username=username, password=password)

        with step("Login with uppercase username"):
            response2 = await auth_client.login(username=username.upper(), password=password)

        with step("Verify one succeeds"):
            assert response1.status_code == 200 or response2.status_code == 200

    @allure.id("DMJS-AUTH-200-011")
    @allure.title("DMJS-AUTH-200-011 - User Data Consistency")
    async def test_user_data_consistency(self, auth_client: AuthClient):
        username = USER_CREDENTIALS["username"]
        password = USER_CREDENTIALS["password"]

        with step("Login"):
            login_response = await auth_client.login(username=username, password=password)
            login_data = login_response.json()

        with step("Get current user"):
            user_response = await auth_client.get_current_user(login_data["accessToken"])
            user_data = user_response.json()

        with step("Verify data consistency"):
            assert login_data["id"] == user_data["id"]
            assert login_data["username"] == user_data["username"]
            assert login_data["email"] == user_data["email"]
            assert user_data["username"] == username
