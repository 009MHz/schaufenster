import asyncio
import pytest
import allure
from utils.__allure_helpers import step
from sources.api.dummyjson.users_client import UsersClient


@pytest.mark.api
@pytest.mark.regression
@allure.epic("DummyJSON API")
@allure.feature("Users")
@allure.story("Users API Endpoints")
class TestDummyUsersAPI:
    @pytest.mark.asyncio
    @allure.id("API-USER-200-001")
    @allure.title("API-USER-200-001 - Get Single User Success")
    async def test_get_single_user(self, users_client: UsersClient):
        with step("Send GET request to /users/1"):
            response = await users_client.get_user(user_id=1)

        with step("Verify response status is 200"):
            assert response.status_code == 200

        with step("Verify user data structure"):
            data = response.json()
            assert data["id"] == 1
            assert "firstName" in data
            assert "lastName" in data
            assert "email" in data
            assert "username" in data

    @pytest.mark.asyncio
    @allure.id("API-USER-200-002")
    @allure.title("API-USER-200-002 - Get Users List with Pagination")
    async def test_get_users_list(self, users_client: UsersClient):
        with step("Get first page of users"):
            response = await users_client.get_users(limit=10, skip=0)

        with step("Verify response structure"):
            assert response.status_code == 200
            data = response.json()
            assert "users" in data
            assert "total" in data
            assert "skip" in data
            assert "limit" in data

        with step("Verify pagination parameters"):
            assert data["limit"] == 10
            assert data["skip"] == 0
            assert len(data["users"]) <= 10

    @pytest.mark.asyncio
    @allure.id("API-USER-200-003")
    @allure.title("API-USER-200-003 - Search Users")
    async def test_search_users(self, users_client: UsersClient):
        with step("Search for users named 'John'"):
            response = await users_client.search_users(query="John")

        with step("Verify search results"):
            assert response.status_code == 200
            data = response.json()
            assert "users" in data

        with step("Verify search relevance"):
            if len(data["users"]) > 0:
                found_relevant = False
                for user in data["users"]:
                    if "john" in user["firstName"].lower() or "john" in user["lastName"].lower():
                        found_relevant = True
                        break
                assert found_relevant, "Search results should contain relevant users"

    @pytest.mark.asyncio
    @allure.id("API-USER-200-004")
    @allure.title("API-USER-200-004 - Filter Users")
    async def test_filter_users(self, users_client: UsersClient):
        with step("Filter users by hair color"):
            response = await users_client.filter_users(key="hair.color", value="Brown")

        with step("Verify filter results"):
            assert response.status_code == 200
            data = response.json()
            assert "users" in data

    @pytest.mark.asyncio
    @allure.id("API-USER-201-001")
    @allure.title("API-USER-201-001 - Create User")
    async def test_create_user(self, users_client: UsersClient):
        user_payload = {
            "firstName": "Test",
            "lastName": "User",
            "age": 30,
            "email": "test.user@example.com",
            "username": "testuser123"
        }

        with step("Create new user"):
            response = await users_client.add_user(user_payload)

        with step("Verify user was created"):
            assert response.status_code == 201
            data = response.json()
            assert "id" in data
            assert data["firstName"] == user_payload["firstName"]
            assert data["lastName"] == user_payload["lastName"]

    @pytest.mark.asyncio
    @allure.id("API-USER-200-005")
    @allure.title("API-USER-200-005 - Update User (PUT)")
    async def test_update_user_put(self, users_client: UsersClient):
        with step("Update user with PUT"):
            update_data = {
                "firstName": "Updated",
                "lastName": "Name",
                "age": 35
            }
            response = await users_client.update_user(
                user_id=1,
                user_data=update_data
            )

        with step("Verify user was updated"):
            assert response.status_code == 200
            data = response.json()
            assert data["firstName"] == "Updated"
            assert data["lastName"] == "Name"

    @pytest.mark.asyncio
    @allure.id("API-USER-200-006")
    @allure.title("API-USER-200-006 - Update User (PATCH)")
    async def test_update_user_patch(self, users_client: UsersClient):
        with step("Partially update user"):
            patch_data = {"firstName": "Patched"}
            response = await users_client.patch_user(
                user_id=1,
                user_data=patch_data
            )

        with step("Verify partial update worked"):
            assert response.status_code == 200
            data = response.json()
            assert data["firstName"] == "Patched"

    @pytest.mark.asyncio
    @allure.id("API-USER-200-007")
    @allure.title("API-USER-200-007 - Delete User")
    async def test_delete_user(self, users_client: UsersClient):
        with step("Delete user"):
            response = await users_client.delete_user(user_id=1)

        with step("Verify user was deleted"):
            assert response.status_code == 200
            data = response.json()
            assert data["isDeleted"] is True
            assert data["deletedOn"] is not None

    @pytest.mark.asyncio
    @allure.id("API-USER-200-008")
    @allure.title("API-USER-200-008 - Concurrent User Requests")
    async def test_concurrent_user_requests(self, users_client: UsersClient):
        with step("Request 5 users concurrently"):
            tasks = [
                users_client.get_user(user_id)
                for user_id in range(1, 6)
            ]
            responses = await asyncio.gather(*tasks)

        with step("Verify all requests succeeded"):
            for response in responses:
                assert response.status_code == 200
                data = response.json()
                assert "id" in data
                assert "firstName" in data

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
    @allure.id("API-USER-200-009")
    @allure.title("API-USER-200-009 - Parameterized User Retrieval")
    async def test_get_user_by_id(self, users_client: UsersClient, user_id):
        with step(f"Get user {user_id}"):
            response = await users_client.get_user(user_id)

        with step(f"Verify user {user_id} data"):
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == user_id

    @pytest.mark.asyncio
    @allure.id("API-USER-404-001")
    @allure.title("API-USER-404-001 - User Not Found")
    async def test_get_nonexistent_user(self, users_client: UsersClient):
        with step("Request non-existent user"):
            response = await users_client.get_user(user_id=9999)

        with step("Verify 404 response"):
            assert response.status_code == 404
            data = response.json()
            assert "message" in data
