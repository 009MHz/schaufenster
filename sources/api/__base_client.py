import os
import httpx
from typing import Dict, Optional, Any
from utils.api_logger import APIObserver


class BaseAPIClient:
    def __init__(
        self,
        base_url: str,
        default_headers: Optional[Dict[str, str]] = None,
        timeout: float = 15.0,
        http2: bool = False):
        
        self.base_url = base_url.rstrip("/")
        self.default_headers = default_headers or {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.timeout = timeout
        self.http2 = http2
        self._sync_client: Optional[httpx.Client] = None
        self._async_client: Optional[httpx.AsyncClient] = None
        self.debug: bool = os.getenv("API_DEBUG_LOG", "").lower() == "true"
        self.observer = APIObserver()

    def _merge_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        result = self.default_headers.copy()
        if headers:
            result.update(headers)
        return result

    def _build_url(self, endpoint: str) -> str:
        return (
            endpoint
            if endpoint.startswith(("http://", "https://"))
            else f"{self.base_url}/{endpoint.lstrip('/')}"
        )

    @property
    def sync_client(self) -> httpx.Client:
        if not self._sync_client:
            self._sync_client = httpx.Client(
                timeout=self.timeout, http2=self.http2, follow_redirects=True)
        return self._sync_client

    @property
    def async_client(self) -> httpx.AsyncClient:
        if not self._async_client:
            self._async_client = httpx.AsyncClient(
                timeout=self.timeout, http2=self.http2, follow_redirects=True)
        return self._async_client

    async def _async_request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        url = self._build_url(endpoint)
        headers = self._merge_headers(kwargs.pop("headers", None))

        if self.debug:
            self.observer.log_request(method, url, headers=headers, **kwargs)
        self.observer.attach_request(method, url, headers=headers, **kwargs)

        response = await getattr(self.async_client, method.lower())(
            url, headers=headers, **kwargs)

        if self.debug:
            self.observer.log_response(response)
        self.observer.attach_response(response)

        return response

    def sync_request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        url = self._build_url(endpoint)
        headers = self._merge_headers(kwargs.pop("headers", None))

        if self.debug:
            self.observer.log_request(method, url, headers=headers, **kwargs)
        self.observer.attach_request(method, url, headers=headers, **kwargs)

        response = getattr(self.sync_client, method.lower())(
            url, headers=headers, **kwargs)

        if self.debug:
            self.observer.log_response(response)
        self.observer.attach_response(response)

        return response

    # ==================== ASYNC Methods ====================
    async def async_get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:
        
        return await self._async_request("GET", endpoint, params=params, headers=headers, **kwargs)

    async def async_post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:
        
        return await self._async_request("POST", endpoint, json=json_data, data=data, headers=headers, **kwargs)

    async def async_put(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:
        
        return await self._async_request("PUT", endpoint, json=json_data, data=data, headers=headers, **kwargs)

    async def async_patch(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:
        
        return await self._async_request("PATCH", endpoint, json=json_data, data=data, headers=headers, **kwargs)

    async def async_delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:
        
        return await self._async_request("DELETE", endpoint, params=params, headers=headers, **kwargs)

    # ==================== SYNC Methods ====================
    def sync_get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:
        
        return self.sync_request("GET", endpoint, params=params, headers=headers, **kwargs)

    def sync_post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:
        
        return self.sync_request("POST", endpoint, json=json_data, data=data, headers=headers, **kwargs)

    def sync_put(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:
        
        return self.sync_request("PUT", endpoint, json=json_data, data=data, headers=headers, **kwargs)

    def sync_patch(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:
        
        return self.sync_request("PATCH", endpoint, json=json_data, data=data, headers=headers, **kwargs)

    def sync_delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:
        
        return self.sync_request("DELETE", endpoint, params=params, headers=headers, **kwargs)

    # ==================== Resource Cleanup ====================
    def close_sync(self) -> None:
        if self._sync_client:
            self._sync_client.close()
            self._sync_client = None

    async def close_async(self) -> None:
        if self._async_client:
            await self._async_client.aclose()
            self._async_client = None

    def close_all(self) -> None:
        self.close_sync()

    async def aclose_all(self) -> None:
        self.close_sync()
        await self.close_async()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_all()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose_all()
