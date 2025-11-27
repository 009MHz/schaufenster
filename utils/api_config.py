import os
from typing import Dict, Any


class APIConfig:
    ENVIRONMENTS = {
        "dev": {
            "base_url": "https://dummyjson.com",
            "timeout": 30000,
        },
        "qa": {
            "base_url": "https://dummyjson.com",
            "timeout": 30000,
        },
        "staging": {
            "base_url": "https://dummyjson.com",
            "timeout": 15000,
        },
        "production": {
            "base_url": "https://dummyjson.com",
            "timeout": 10000,
        },
    }

    @classmethod
    def get_config(cls, env: str = "") -> Dict[str, Any]:
        """
        Get configuration for specified environment.

        Args:
            env: Environment name (dev, qa, staging, production)

        Returns:
            Environment configuration dictionary
        """
        if env == "":
            env = os.getenv("TEST_ENV", "dev")

        env = env.lower()
        return cls.ENVIRONMENTS.get(env, cls.ENVIRONMENTS["dev"])

    @classmethod
    def get_base_url(cls, env: str) -> str:
        """
        Get base URL for specified environment.

        Args:
            env: Environment name

        Returns:
            Base URL string
        """
        config = cls.get_config(env)
        return config["base_url"]

    @classmethod
    def get_timeout(cls, env: str = "") -> int:
        """
        Get request timeout for specified environment.

        Args:
            env: Environment name

        Returns:
            Timeout in milliseconds
        """
        config = cls.get_config(env)
        return config["timeout"]
