import pytest
import allure
from utils.__allure_helpers import step
from sources.api.dummyjson.auth_client import AuthClient


@pytest.mark.api
@pytest.mark.regression
@allure.epic("DummyJSON API")
@allure.feature("Authentication")
@allure.story("Edge Cases")
class TestAuthEdgeCases:

    @allure.id("DMJS-AUTH-400-006")
    @allure.title("DMJS-AUTH-400-006 - Login with Special Characters")
    async def test_login_special_chars(self, auth_client: AuthClient):
        with step("Attempt login with special characters"):
            response = await auth_client.login(username="user@test#123", password="anypass")

        with step("Verify error response"):
            assert response.status_code == 400

    @allure.id("DMJS-AUTH-400-007")
    @allure.title("DMJS-AUTH-400-007 - Login with Very Long Username")
    async def test_login_long_username(self, auth_client: AuthClient):
        with step("Attempt login with 1000 character username"):
            response = await auth_client.login(username="a" * 1000, password="anypass")

        with step("Verify error response"):
            assert response.status_code == 400

    @allure.id("DMJS-AUTH-400-008")
    @allure.title("DMJS-AUTH-400-008 - Login with Very Long Password")
    async def test_login_long_password(self, auth_client: AuthClient):
        with step("Attempt login with 1000 character password"):
            response = await auth_client.login(username="emilys", password="p" * 1000)

        with step("Verify error response"):
            assert response.status_code == 400

    @allure.id("DMJS-AUTH-400-009")
    @allure.title("DMJS-AUTH-400-009 - Login with Unicode Characters")
    async def test_login_unicode_characters(self, auth_client: AuthClient):
        with step("Attempt login with unicode username"):
            response = await auth_client.login(username="用户名", password="anypass")

        with step("Verify error response"):
            assert response.status_code == 400
