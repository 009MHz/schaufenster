"""
API Test Fixtures.

Provides API client fixtures with centralized resource cleanup.

Architecture:
- Session-scoped config fixtures (base_url, timeout) from --test-env CLI option
- Function-scoped client fixtures with automatic cleanup via registry pattern
- Autouse cleanup fixture ensures all HTTP connections close after each test

Cleanup Strategy:
- All clients registered via setup_client() are tracked in _api_clients list
- _cleanup_api_clients fixture (autouse=True) automatically closes all clients after each test
- No manual yield/cleanup needed in individual fixtures

Usage:
    async def test_example(products_client):
        response = await products_client.async_get_product(1)
        # Client automatically cleaned up after test
"""

import pytest
from typing import List
from sources.api.__base_client import BaseAPIClient
from utils.api_config import APIConfig


# ==================== Cleanup Registry ====================

_api_clients: List[BaseAPIClient] = []


@pytest.fixture(scope="function", autouse=True)
async def _cleanup_api_clients():
    """
    Automatically cleanup all API clients after each test.

    This fixture runs for EVERY test automatically (autouse=True).
    It ensures all HTTP connections are properly closed to prevent resource leaks.
    """
    yield  # Test runs here

    for client in _api_clients:  # Cleanup phase - runs after every test
        try:
            await client.close_async()
        except Exception as e:
            print(f"Warning: Failed to cleanup client {client.__class__.__name__}: {e}")

    _api_clients.clear()


def setup_client(client: BaseAPIClient) -> BaseAPIClient:
    """
    Register API client for automatic cleanup.

    All clients registered via this function will be automatically
    closed after the test completes via the _cleanup_api_clients fixture.
    """
    _api_clients.append(client)
    return client


# ==================== Configuration Fixtures ====================
@pytest.fixture(scope="session")
def api_base_url(request):
    """Get API base URL from configuration based on --test-env CLI option."""
    env = request.config.getoption("--test-env", default="dev")
    return APIConfig.get_base_url(env)


@pytest.fixture(scope="session")
def api_timeout(request):
    """Get API timeout from configuration (converted to seconds)."""
    env = request.config.getoption("--test-env", default="dev")
    return APIConfig.get_timeout(env) / 1000


# ==================== Client Fixtures ====================


@pytest.fixture(scope="function")
async def products_client(api_base_url, api_timeout):
    from sources.api.dummyjson.products_client import ProductsClient

    return setup_client(
        ProductsClient(base_url=api_base_url, timeout=api_timeout)
    )


@pytest.fixture(scope="function")
async def users_client(api_base_url, api_timeout):
    """Users API client with automatic cleanup."""
    from sources.api.dummyjson.users_client import UsersClient

    return setup_client(
        UsersClient(base_url=api_base_url, timeout=api_timeout)
    )


@pytest.fixture(scope="function")
async def auth_client(api_base_url, api_timeout):
    """Auth API client with automatic cleanup."""
    from sources.api.dummyjson.auth_client import AuthClient

    return setup_client(
        AuthClient(base_url=api_base_url, timeout=api_timeout)
    )
