from dataclasses import dataclass
from px_settings.contrib.django import settings as s


__all__ = 'Settings', 'settings',


@s('WCD_JWT_REGISTRY')
@dataclass
class Settings:
    """
    Example:

    ```python
    WCD_JWT_REGISTRY = {
        'TOKEN_EXPIRE_SERIALIZER': 'wcd_jwt.contrib.registry.serializers.TokenExpireSerializer',
    }
    ```
    """
    TOKEN_EXPIRE_SERIALIZER: str = 'wcd_jwt.contrib.registry.serializers.TokenExpireSerializer'


settings = Settings()
