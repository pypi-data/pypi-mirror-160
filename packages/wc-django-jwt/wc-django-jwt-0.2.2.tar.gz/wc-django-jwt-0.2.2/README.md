# WebCase django JWT authentication

Based on [djangorestframework-simplejwt](https://pypi.org/project/djangorestframework-simplejwt/) with a little bit of additional goodies.

Us it's documentation as a source of truth. All changes and additional info about configuration are described here, in this documentation.

## Installation

```sh
pip install wc-django-jwt
```

In `settings.py`:

```python
INSTALLED_APPS += [
  'rest_framework_simplejwt',

  'wcd_jwt',
]

WCD_JWT = {
  # Serializer class for JWT token.
  'TOKEN_OBTAIN_SERIALIZER': 'wcd_jwt.serializers.TokenObtainPairSerializer',
  # Serializer class for JWT token refresh.
  'TOKEN_REFRESH_SERIALIZER': 'wcd_jwt.serializers.TokenRefreshSerializer',

  # Authentication class that will be used by auth middleware to check tokens.
  'AUTHENTICATION_CLASS': 'wcd_jwt.authentication.JWTAuthentication',
  # Available token types to match on.
  'TOKEN_TYPES': [
    'rest_framework_simplejwt.tokens.AccessToken',
    'rest_framework_simplejwt.tokens.RefreshToken',
  ],
  # Should you rotate refresh tokens on access refresh.
  'ROTATE_REFRESH_TOKENS': False,
  # Should you update lsat login field on user on token obtain call.
  'UPDATE_LAST_LOGIN': False,
}

MIDDLEWARE = [
  ...
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  ...
  # Authentication middleware must be placed after django's
  # `AuthenticationMiddleware`.
  'wcd_jwt.middleware.AuthenticationMiddleware',
  ...
]
```

There are ready for use frontend for django rest framework. It mostly provided by `djangorestframework-simplejwt` with some additional changes.

In `urls.py`:

```python
from wcd_jwt.views import make_urlpatterns as jwt_make_urlpatterns

urlpatters = [
  ...
  path(
    'api/v1/auth/token/',
    include((jwt_make_urlpatterns(), 'wcd_jwt'),
    namespace='jwt-auth')
  ),
]
```

And after all that manipulations you end up with 4 views for jwt tokens authentication.

Function `make_urlpatterns` can take your custom views and replace default ones.

## Token registry

Tokens by default are generate-and-forget things. In case you need to remember what tokens were created and for what users there is a contrib package added: `wcd_jwt.contrib.registry`.

It registers all your generated tokens. And may be used to force-expire any of them.

In `settings.py`:

```python
INSTALLED_APPS += [
  'rest_framework_simplejwt',

  'wcd_jwt',
  'wcd_jwt.contrib.registry',
]

WCD_JWT = {
  # Serializer class for JWT token refresh should be changed to:
  'TOKEN_REFRESH_SERIALIZER': 'wcd_jwt.contrib.registry.serializers.TokenRefreshSerializer',

  # If you want to block user not after trey'r access token expired, but
  # at any time they made request change authentication class to:
  'AUTHENTICATION_CLASS': 'wcd_jwt.contrib.registry.authentication.JWTAuthentication',
}

WCD_JWT_REGISTRY = {
  # Token expire serializer may be replaced like this:
  'TOKEN_EXPIRE_SERIALIZER': 'wcd_jwt.contrib.registry.serializers.TokenExpireSerializer',
}
```

The same for urls.

In `urls.py`:

```python
from wcd_jwt.contrib.registry.views import make_urlpatterns as jwt_registry_make_urlpatterns

urlpatters = [
  ...
  path(
    'api/v1/auth/token/',
    include((jwt_registry_make_urlpatterns(), 'wcd_jwt_registry'),
    namespace='jwt-auth-registry')
  ),
]
```

Registry provides 2 models:
- `Token` - Stores information about generated tokens. They are hierarchical. Hierarchy is based on which token was used to generate those from response. Refresh token will always be a parent for access token.
- `TokenUserConnection` - Connects user to token model.

There is only one view at the moment that adds ability to expire any valid token.

To display tokens on the client you may made your own views. Package will not provide them, because there certainly will be additional logic to display, so wer'e not event bothering ourselves).

Tokens has some query methods to made querying easier:

```python
list_of_expired_tokens = Token.objects.expired()
list_of_active_tokens = Token.objects.active()

# Method `collect_tree` we can collect all the ids from token related trees
# for any number of tokens we wish.
# Here we collecting tree ids for some `token1`.
list_of_ids_for_all_the_token_relatives_tree = Token.objects.collect_tree(
  ids=[token1.id]
)

# We may easily find tokens for a certain user:
list_of_users_tokens = Token.objects.filter(
  user_connections__user=some_user_instance
)

# etc.
```
