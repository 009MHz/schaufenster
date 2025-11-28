import pytest
import allure
from utils.__allure_helpers import step
from sources.api.dummyjson.auth_client import AuthClient


@pytest.mark.api
@pytest.mark.security
@allure.epic("DummyJSON API")
@allure.feature("Authentication")
@allure.story("Security Tests")
class TestAuthSecurity:

    @allure.id("DMJS-AUTH-400-010")
    @allure.title("DMJS-AUTH-400-010 - SQL Injection Attempt")
    async def test_sql_injection_username(self, auth_client: AuthClient):
        with step("Attempt login with SQL injection payload"):
            response = await auth_client.login(username="' OR '1'='1", password="anypass")

        with step("Verify injection blocked"):
            assert response.status_code == 400

    @allure.id("DMJS-AUTH-400-011")
    @allure.title("DMJS-AUTH-400-011 - XSS Attempt")
    async def test_xss_attempt_username(self, auth_client: AuthClient):
        with step("Attempt login with XSS payload"):
            response = await auth_client.login(username="<script>alert('XSS')</script>", password="anypass")

        with step("Verify XSS blocked"):
            assert response.status_code == 400

    @allure.id("DMJS-AUTH-401-004")
    @allure.title("DMJS-AUTH-401-004 - JWT Token Tampering")
    async def test_jwt_token_tampering(self, auth_client: AuthClient):
        with step("Login to get valid token"):
            login_response = await auth_client.login(username="emilys", password="emilyspass")
            access_token = login_response.json()["accessToken"]

        with step("Tamper with token"):
            tampered_token = access_token[:-10] + "X" + access_token[-9:]

        with step("Attempt to use tampered token"):
            response = await auth_client.get_current_user(tampered_token)

        with step("Verify tampered token rejected"):
            assert response.status_code in [401, 500]
