import os
import json
import copy
import httpx
import allure
from typing import Dict, Optional, Any
from allure_commons.types import AttachmentType


class BaseAPIClient:
    """Base HTTP client with sync and async methods."""

    SENSITIVE_FIELDS = [
        "password",
        "token",
        "accessToken",
        "access_token",
        "refreshToken",
        "refresh_token",
        "apiKey",
        "api_key",
        "secret",
        "authorization",
        "Authorization",
    ]

    def __init__(
        self,
        base_url: str,
        default_headers: Optional[Dict[str, str]] = None,
        timeout: float = 15.0,
        http2: bool = False,
    ):
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
        if not self._sync_client:self._sync_client = httpx.Client(
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
            self._log_request(method, url, headers=headers, **kwargs)
        self._attach_allure_request(method, url, headers=headers, **kwargs)

        response = await getattr(self.async_client, method.lower())(
            url, headers=headers, **kwargs)

        if self.debug:
            self._log_response(response)
        self._attach_allure_response(response)

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

        url, headers = self._build_url(endpoint), self._merge_headers(headers)
        return self.sync_client.get(url, params=params, headers=headers, **kwargs)

    def sync_post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:
        
        url, headers = self._build_url(endpoint), self._merge_headers(headers)
        return self.sync_client.post(url, json=json_data, data=data, headers=headers, **kwargs)

    def sync_put(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:

        url, headers = self._build_url(endpoint), self._merge_headers(headers)
        return self.sync_client.put(url, json=json_data, data=data, headers=headers, **kwargs)

    def sync_patch(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:

        url, headers = self._build_url(endpoint), self._merge_headers(headers)
        return self.sync_client.patch(url, json=json_data, data=data, headers=headers, **kwargs)

    def sync_delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs) -> httpx.Response:

        url, headers = self._build_url(endpoint), self._merge_headers(headers)
        return self.sync_client.delete(url, params=params, headers=headers, **kwargs)

    # ==================== Response Helpers ====================
    @staticmethod
    def get_json(response: httpx.Response) -> Dict[str, Any]:
        return response.json()

    @staticmethod
    def get_text(response: httpx.Response) -> str:
        return response.text

    @staticmethod
    def get_status(response: httpx.Response) -> int:
        return response.status_code

    @staticmethod
    def get_headers(response: httpx.Response) -> httpx.Headers:
        return response.headers

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


    # ==================== Debug & Allure ====================
    def _log_request(self, method: str, url: str, **kwargs):
        """Terminal debug logging for requests."""
        print(f"\n{'='*80}\n[API REQUEST] {method} {url}\n{'='*80}\n")
        body = kwargs.get("json_data") or kwargs.get("data") or kwargs.get("params")
        if body:
            print(
                json.dumps(body, indent=2, ensure_ascii=False)
                if isinstance(body, dict)
                else f"Params: {body}"
            )

    def _log_response(self, response: httpx.Response):
        """Terminal debug logging for responses."""
        print(f"\n{'='*80}\n[API RESPONSE]: {response.status_code}\n{'='*80}\n")
        try:
            print(json.dumps(json.loads(response.text), indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(response.text)
        except Exception as e:
            print(f"[ERROR] {e}")
        print()

    def _mask_sensitive_data(self, data: Any) -> Any:
        """Recursively mask sensitive fields for Allure."""
        if isinstance(data, list):
            return [self._mask_sensitive_data(item) for item in data]
        if not isinstance(data, dict):
            return data
        masked = copy.deepcopy(data)
        for key, value in masked.items():
            if key in self.SENSITIVE_FIELDS:
                masked[key] = "***MASKED***"
            elif isinstance(value, (dict, list)):
                masked[key] = self._mask_sensitive_data(value)
        return masked

    def _attach_allure_request(self, method: str, url: str, **kwargs):
        """Attach request to Allure (masked)."""
        try:
            data = {
                "method": method,
                "url": url,
                "headers": dict(kwargs.get("headers", {})),
            }
            if "Authorization" in data["headers"]:
                data["headers"]["Authorization"] = "***MASKED***"
            if "json_data" in kwargs and kwargs["json_data"]:
                data["body"] = self._mask_sensitive_data(kwargs["json_data"])
            elif "data" in kwargs and kwargs["data"]:
                data["body"] = self._mask_sensitive_data(kwargs["data"])
            if "params" in kwargs and kwargs["params"]:
                data["params"] = self._mask_sensitive_data(kwargs["params"])
            allure.attach(
                json.dumps(data, indent=2, ensure_ascii=False),
                name=f"Request - {method} {url}",
                attachment_type=AttachmentType.JSON,
            )
        except:
            pass

    def _attach_allure_response(self, response: httpx.Response):
        """Attach response to Allure (masked)."""
        try:
            # Metadata
            metadata = {
                "status": response.status_code,
                "url": str(response.url),
                "headers": dict(response.headers),
            }
            for header in ["set-cookie", "authorization"]:
                if header in metadata["headers"]:
                    metadata["headers"][header] = "***MASKED***"
            allure.attach(
                json.dumps(metadata, indent=2, ensure_ascii=False),
                name=f"Response Metadata - {response.status_code}",
                attachment_type=AttachmentType.JSON,
            )

            try:
                body = self._mask_sensitive_data(json.loads(response.text))
                allure.attach(
                    json.dumps(body, indent=2, ensure_ascii=False),
                    name=f"Response Body - {response.status_code}",
                    attachment_type=AttachmentType.JSON,
                )
            except json.JSONDecodeError:
                allure.attach(
                    response.text,
                    name=f"Response Body - {response.status_code}",
                    attachment_type=AttachmentType.TEXT,
                )
        except:
            pass
