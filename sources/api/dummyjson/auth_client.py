import httpx
from typing import Dict, Any, Optional
from sources.api.__base_client import BaseAPIClient


class AuthClient(BaseAPIClient):
    def __init__(self, base_url: str, **kwargs):
        super().__init__(base_url, **kwargs)

    # ==================== ASYNC Methods ====================

    async def login(self, username: str, password: str, expires_in_mins: int = 30) -> httpx.Response:
        """
        Args:
            username: Username (e.g., 'emilys')
            password: Password (e.g., 'emilyspass')
            expires_in_mins: Token expiration in minutes (default: 30)
        """
        payload = {
            "username": username,
            "password": password,
            "expiresInMins": expires_in_mins
        }
        return await self.async_post("/auth/login", json_data=payload)

    async def get_current_user(self, access_token: str) -> httpx.Response:
        """
        Args:
            access_token: JWT access token from login
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        return await self.async_get("/auth/me", headers=headers)

    async def refresh_token(self, refresh_token: str, expires_in_mins: int = 30) -> httpx.Response:
        """
        Args:
            refresh_token: Refresh token from login
            expires_in_mins: New token expiration in minutes (default: 30)
        """
        payload = {
            "refreshToken": refresh_token,
            "expiresInMins": expires_in_mins
        }
        return await self.async_post("/auth/refresh", json_data=payload)

