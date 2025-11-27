import asyncio
import pytest
import allure
from utils.__allure_helpers import step
from sources.api.dummyjson.products_client import ProductsClient


@pytest.mark.api
@pytest.mark.regression
@allure.epic("DummyJSON API")
@allure.feature("Products")
@allure.story("Products API Endpoints")
class TestDummyProductsAPI:
    @allure.id("API-PROD-200-001")
    @allure.title("API-PROD-200-001 - Get Single Product Success")
    async def test_get_single_product(self, products_client: ProductsClient):
        with step("Send GET request to /products/1"):
            response = await products_client.get_product(product_id=1)

        with step("Verify response status is 200"):
            assert response.status_code == 200

        with step("Verify product data structure"):
            data = response.json()
            assert data["id"] == 1
            assert "title" in data
            assert "description" in data
            assert "price" in data
            assert "category" in data
    
    @allure.id("API-PROD-200-002")
    @allure.title("API-PROD-200-002 - Get Products List with Pagination")
    async def test_get_products_list(self, products_client: ProductsClient):
        with step("Get first page of products"):
            response = await products_client.get_products(limit=10, skip=0)

        with step("Verify response structure"):
            assert response.status_code == 200
            data = response.json()
            assert "products" in data
            assert "total" in data
            assert "skip" in data
            assert "limit" in data

        with step("Verify pagination parameters"):
            assert data["limit"] == 10
            assert data["skip"] == 0
            assert len(data["products"]) <= 10
    
    @allure.id("API-PROD-200-003")
    @allure.title("API-PROD-200-003 - Search Products")
    async def test_search_products(self, products_client: ProductsClient):
        with step("Search for 'phone' products"):
            response = await products_client.search_products(query="phone")

        with step("Verify search results"):
            assert response.status_code == 200
            data = response.json()
            assert "products" in data
            assert len(data["products"]) > 0

        with step("Verify search relevance"):
            found_relevant = False
            for product in data["products"]:
                if "phone" in product["title"].lower() or "phone" in product["description"].lower():
                    found_relevant = True
                    break
            assert found_relevant, "Search results should contain relevant products"
    
    @allure.id("API-PROD-200-004")
    @allure.title("API-PROD-200-004 - Get Product Categories")
    async def test_get_categories(self, products_client: ProductsClient):
        with step("Get categories list"):
            response = await products_client.get_product_categories()

        with step("Verify categories response"):
            assert response.status_code == 200
            categories = response.json()
            assert isinstance(categories, list)
            assert len(categories) > 0
    
    @allure.id("API-PROD-200-005")
    @allure.title("API-PROD-200-005 - Get Products by Category")
    async def test_get_products_by_category(self, products_client: ProductsClient):
        with step("Get products in 'smartphones' category"):
            response = await products_client.get_products_by_category(category="smartphones")

        with step("Verify category filter works"):
            assert response.status_code == 200
            data = response.json()
            assert "products" in data
            assert len(data["products"]) > 0

        with step("Verify all products belong to category"):
            for product in data["products"]:
                assert product["category"] == "smartphones"
    
    @allure.id("API-PROD-201-001")
    @allure.title("API-PROD-201-001 - Create Product")
    async def test_create_product(self, products_client: ProductsClient):
        product_payload = {
            "title": "Test Product",
            "description": "Test product description for API testing",
            "price": 99.99,
            "category": "electronics",
            "brand": "TestBrand"
        }

        with step("Create new product"):
            response = await products_client.add_product(product_payload)

        with step("Verify product was created"):
            assert response.status_code == 201
            data = response.json()
            assert "id" in data
            assert data["title"] == product_payload["title"]
            assert data["price"] == product_payload["price"]
    
    @allure.id("API-PROD-200-006")
    @allure.title("API-PROD-200-006 - Update Product (PUT)")
    async def test_update_product_put(self, products_client: ProductsClient):
        with step("Update product with PUT"):
            update_data = {
                "title": "Updated Product Title",
                "price": 149.99
            }
            response = await products_client.update_product(
                product_id=1,
                product_data=update_data
            )

        with step("Verify product was updated"):
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Updated Product Title"
            assert data["price"] == 149.99
    
    @allure.id("API-PROD-200-007")
    @allure.title("API-PROD-200-007 - Update Product (PATCH)")
    async def test_update_product_patch(self, products_client: ProductsClient):
        with step("Partially update product"):
            patch_data = {"title": "Patched Title"}
            response = await products_client.patch_product(
                product_id=1,
                product_data=patch_data
            )

        with step("Verify partial update worked"):
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Patched Title"
    
    @allure.id("API-PROD-200-008")
    @allure.title("API-PROD-200-008 - Delete Product")
    async def test_delete_product(self, products_client: ProductsClient):
        with step("Delete product"):
            response = await products_client.delete_product(product_id=1)

        with step("Verify product was deleted"):
            assert response.status_code == 200
            data = response.json()
            assert data["isDeleted"] is True
            assert data["deletedOn"] is not None
    
    @allure.id("API-PROD-200-009")
    @allure.title("API-PROD-200-009 - Concurrent Product Requests")
    async def test_concurrent_product_requests(self, products_client: ProductsClient):
        with step("Request 5 products concurrently"):
            tasks = [
                products_client.get_product(product_id)
                for product_id in range(1, 6)
            ]
            responses = await asyncio.gather(*tasks)

        with step("Verify all requests succeeded"):
            for response in responses:
                assert response.status_code == 200
                data = response.json()
                assert "id" in data
                assert "title" in data
    
    @allure.id("API-PROD-200-010")
    @allure.title("API-PROD-200-010 - Concurrent Search Requests")
    async def test_concurrent_search_requests(self, products_client: ProductsClient):
        with step("Perform concurrent searches"):
            search_terms = ["phone", "laptop", "shirt", "watch", "perfume"]
            tasks = [
                products_client.search_products(query)
                for query in search_terms
            ]
            responses = await asyncio.gather(*tasks)

        with step("Verify all searches succeeded"):
            for response in responses:
                assert response.status_code == 200
                data = response.json()
                assert "products" in data
    
    @pytest.mark.parametrize("product_id", [1, 2, 3, 4, 5])
    @allure.id("API-PROD-200-011")
    @allure.title("API-PROD-200-011 - Parameterized Product Retrieval")
    async def test_get_product_by_id(self, products_client: ProductsClient, product_id):
        with step(f"Get product {product_id}"):
            response = await products_client.get_product(product_id)

        with step(f"Verify product {product_id} data"):
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == product_id
    
    @allure.id("API-PROD-404-001")
    @allure.title("API-PROD-404-001 - Product Not Found")
    async def test_get_nonexistent_product(self, products_client: ProductsClient):
        with step("Request non-existent product"):
            response = await products_client.get_product(product_id=9999)

        with step("Verify 404 response"):
            assert response.status_code == 404
            data = response.json()
            assert "message" in data
    
    @allure.id("API-PROD-200-012")
    @allure.title("API-PROD-200-012 - Search with No Results")
    async def test_search_no_results(self, products_client: ProductsClient):
        with step("Search for non-existent term"):
            response = await products_client.search_products(query="xyznonexistent123")

        with step("Verify empty results"):
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 0
            assert len(data["products"]) == 0
