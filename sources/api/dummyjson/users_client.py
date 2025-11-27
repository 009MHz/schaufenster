import httpx
from typing import Dict, Any, Optional
from sources.api.__base_client import BaseAPIClient


class UsersClient(BaseAPIClient):
    def __init__(self, base_url: str, **kwargs):
        super().__init__(base_url, **kwargs)

    async def get_users(self, limit: int = 30, skip: int = 0) -> httpx.Response:
        """
        Get paginated list of users (async).

        Args:
            limit: Number of users to return (default: 30)
            skip: Number of users to skip (default: 0)
        """
        return await self.async_get("/users", params={"limit": limit, "skip": skip})

    async def get_user(self, user_id: int) -> httpx.Response:
        """
        Get single user by ID (async).

        Args:
            user_id: User ID
        """
        return await self.async_get(f"/users/{user_id}")

    async def search_users(self, query: str) -> httpx.Response:
        """
        Search users by query (async).

        Args:
            query: Search query (searches firstName and lastName)
        """
        return await self.async_get("/users/search", params={"q": query})

    async def filter_users(self, key: str, value: str) -> httpx.Response:
        """
        Filter users by key-value pair (async).

        Args:
            key: Filter key (e.g., 'hair.color', 'age')
            value: Filter value
        """
        return await self.async_get("/users/filter", params={"key": key, "value": value})

    async def add_user(self, user_data: Dict[str, Any]) -> httpx.Response:
        """
        Add new user (async).

        Note: This is a mock endpoint - data is not actually persisted.

        Args:
            user_data: User data (firstName, lastName, age, etc.) with created user data (including ID)
        """
        return await self.async_post("/users/add", json_data=user_data)

    async def update_user(
        self, user_id: int, user_data: Dict[str, Any]
    ) -> httpx.Response:
        """
        Update user with PUT (async) - replaces entire resource.

        Note: This is a mock endpoint - data is not actually updated.

        Args:
            user_id: User ID
            user_data: Updated user data
        """
        return await self.async_put(f"/users/{user_id}", json_data=user_data)

    async def patch_user(
        self, user_id: int, user_data: Dict[str, Any]
    ) -> httpx.Response:
        """
        Update user with PATCH (async) - partial update.

        Note: This is a mock endpoint - data is not actually updated.

        Args:
            user_id: User ID
            user_data: Partial user data to update
        """
        return await self.async_patch(f"/users/{user_id}", json_data=user_data)

    async def delete_user(self, user_id: int) -> httpx.Response:
        """
        Delete user (async).

        Note: This is a mock endpoint - data is not actually deleted.

        Args:
            user_id: User ID with deleted user info
        """
        return await self.async_delete(f"/users/{user_id}")

