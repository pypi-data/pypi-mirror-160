from rest_framework_simplejwt.tokens import Token as TokenStruct
from rest_framework_simplejwt.settings import api_settings


def get_token_jti(token: TokenStruct) -> str:
    return token.payload[api_settings.JTI_CLAIM]
