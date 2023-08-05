from typing import List, Sequence

# FIXME: This should not be here!
from wcd_device_recognizer.utils import model_bulk_get_or_create

from ..models import TokenUserConnection, Token


def connect(user, tokens: Sequence[Token]) -> List[TokenUserConnection]:
    uniques = {(user.pk, token.pk) for token in tokens}

    return model_bulk_get_or_create(TokenUserConnection, [
        ({'user_id': uid, 'token_id': tid}, {})
        for uid, tid in uniques
    ])
