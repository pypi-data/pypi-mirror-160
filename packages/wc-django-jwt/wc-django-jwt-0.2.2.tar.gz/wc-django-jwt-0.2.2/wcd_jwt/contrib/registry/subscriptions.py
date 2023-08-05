from django.dispatch import receiver
from wcd_jwt.signals import token_refreshed, token_obtained
from django.contrib.auth import get_user_model

from .services import token_manager, user_connector


def _flat(pairs):
    return [y for x in pairs for y in x]


@receiver(token_obtained)
def register_token_on_obtain(sender, serializer, result, **kwargs):
    # TODO: Make this in a separate thread or even in celery.
    v = serializer.validated_data

    pairs = token_manager.register((
        (v['access'], v['refresh']),
    ))

    # Connecting users if possible.
    if 'user' in serializer.validated_data:
        user_connector.connect(
            serializer.validated_data['user'], _flat(pairs)
        )


@receiver(token_refreshed)
def register_token_on_refresh(sender, serializer, result, **kwargs):
    # TODO: Make this in a separate thread or even in celery.
    v = serializer.validated_data
    token_class = serializer.token_class
    base = v['refresh']
    pairs = [(v['access'], base)]

    if 'refresh' in result:
        refresh = token_class(result['refresh'])
        pairs = (
            # Wer'e replacing access token parent with newly generated refresh.
            # It's because we want to form a straight relation between
            # responded refresh->access tokens.
            (v['access'], refresh),
            (refresh, base),
        )

    pairs = token_manager.register(pairs)

    # Searching for user connections of the previous token(s).
    # To connect them. If there is more than one user - something
    # wrong happened and no connection will be established.
    users = list(
        get_user_model().objects
        .filter(token_connections__token__in=_flat(pairs))
    )
    if len(users) == 1:
        user_connector.connect(users[0], _flat(pairs))
