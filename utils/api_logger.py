import json
import copy
import httpx
import allure
from typing import Any
from allure_commons.types import AttachmentType


class APIObserver:
    """Handles debug logging and Allure reporting for API requests/responses."""

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

    @staticmethod
    def log_request(method: str, url: str, **kwargs):
        """Terminal debug logging for requests."""
        print(f"\n{'='*80}\n[API REQUEST] {method} {url}\n{'='*80}\n")
        body = kwargs.get("json") or kwargs.get("data") or kwargs.get("params")
        if body:
            print(
                json.dumps(body, indent=2, ensure_ascii=False)
                if isinstance(body, dict)
                else f"Params: {body}"
            )

    @staticmethod
    def log_response(response: httpx.Response):
        """Terminal debug logging for responses."""
        print(f"\n{'='*80}\n[API RESPONSE]: {response.status_code}\n{'='*80}\n")
        try:
            print(json.dumps(json.loads(response.text), indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(response.text)
        except Exception as e:
            print(f"[ERROR] {e}")
        print()

    @classmethod
    def mask_sensitive_data(cls, data: Any) -> Any:
        """Recursively mask sensitive fields for Allure."""
        if isinstance(data, list):
            return [cls.mask_sensitive_data(item) for item in data]
        if not isinstance(data, dict):
            return data
        masked = copy.deepcopy(data)
        for key, value in masked.items():
            if key in cls.SENSITIVE_FIELDS:
                masked[key] = "***MASKED***"
            elif isinstance(value, (dict, list)):
                masked[key] = cls.mask_sensitive_data(value)
        return masked

    @classmethod
    def attach_request(cls, method: str, url: str, **kwargs):
        """Attach request to Allure (masked)."""
        try:
            data = {
                "method": method,
                "url": url,
                "headers": dict(kwargs.get("headers", {})),
            }
            if "Authorization" in data["headers"]:
                data["headers"]["Authorization"] = "***MASKED***"
            if "json" in kwargs and kwargs["json"]:
                data["body"] = cls.mask_sensitive_data(kwargs["json"])
            elif "data" in kwargs and kwargs["data"]:
                data["body"] = cls.mask_sensitive_data(kwargs["data"])
            if "params" in kwargs and kwargs["params"]:
                data["params"] = cls.mask_sensitive_data(kwargs["params"])
            allure.attach(
                json.dumps(data, indent=2, ensure_ascii=False),
                name=f"Request - {method} {url}",
                attachment_type=AttachmentType.JSON,
            )
        except:
            pass

    @classmethod
    def attach_response(cls, response: httpx.Response):
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
                body = cls.mask_sensitive_data(json.loads(response.text))
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
