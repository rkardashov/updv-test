from django.http import JsonResponse
from rest_framework import status

from api.models import ExpirableToken


class TokenLifetimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != '/login':
            header = request.META.get('HTTP_AUTHORIZATION')
            if header and header.startswith('Bearer '):
                token_key = header.split(' ')[1]
                try:
                    token = ExpirableToken.objects.get(key=token_key)
                    if token.is_expired:
                        return JsonResponse({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
                    token.save()

                except ExpirableToken.DoesNotExist:
                    return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        return self.get_response(request)