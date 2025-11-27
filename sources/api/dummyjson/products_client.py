import httpx
from typing import Dict, Any, Optional
from sources.api.__base_client import BaseAPIClient


class ProductsClient(BaseAPIClient):
    def __init__(self, base_url: str, **kwargs):
        """
        Initialize Products API client.

        Args:
            base_url: Base URL for API (e.g., "https://dummyjson.com")
            **kwargs: Additional arguments for BaseAPIClient
        """
        super().__init__(base_url, **kwargs)

    # ==================== ASYNC Methods ====================

    async def get_products(
        self, limit: int = 30, skip: int = 0
    ) -> httpx.Response:
        """
        Get paginated list of products (async).

        Args:
            limit: Number of products to return (default: 30)
            skip: Number of products to skip (default: 0)
        """
        return await self.async_get("/products", params={"limit": limit, "skip": skip})

    async def get_product(self, product_id: int) -> httpx.Response:
        """
        Get single product by ID (async).

        Args:
            product_id: Product ID

        """
        return await self.async_get(f"/products/{product_id}")

    async def search_products(self, query: str) -> httpx.Response:
        """
        Search products by query (async).

        Args:
            query: Search query

        """
        return await self.async_get("/products/search", params={"q": query})

    async def get_product_categories(self) -> httpx.Response:
        """
        Get list of product categories with list of categories
        """
        return await self.async_get("/products/categories")

    async def get_products_by_category(self, category: str) -> httpx.Response:
        """
        Get products by category (async).

        Args:
            category: Category name
        """
        return await self.async_get(f"/products/category/{category}")

    async def add_product(self, product_data: Dict[str, Any]) -> httpx.Response:
        """
        Add new product (async).

        Note: This is a mock endpoint - data is not actually persisted.

        Args:
            product_data: Product data (title, description, price, etc.)
            with created product data (including ID)
        """
        return await self.async_post("/products/add", json_data=product_data)

    async def update_product(
        self, product_id: int, product_data: Dict[str, Any]
    ) -> httpx.Response:
        """
        Update product with PUT (async) - replaces entire resource.

        Note: This is a mock endpoint - data is not actually updated.

        Args:
            product_id: Product ID
            product_data: Updated product data
        """
        return await self.async_put(f"/products/{product_id}", json_data=product_data)

    async def patch_product(
        self, product_id: int, product_data: Dict[str, Any]
    ) -> httpx.Response:
        """
        Update product with PATCH (async) - partial update.

        Note: This is a mock endpoint - data is not actually updated.

        Args:
            product_id: Product ID
            product_data: Partial product data to update
        """
        return await self.async_patch(f"/products/{product_id}", json_data=product_data)

    async def delete_product(self, product_id: int) -> httpx.Response:
        """
        Delete product (async).

        Note: This is a mock endpoint - data is not actually deleted.

        Args:
            product_id: Product ID 
        """
        return await self.async_delete(f"/products/{product_id}")
