from rest_framework.authentication import TokenAuthentication

from .models import ExpirableToken


class BearerTokenAuthentication(TokenAuthentication):
    model = ExpirableToken
    keyword = 'Bearer'
