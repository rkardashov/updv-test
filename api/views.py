import requests
from time import time

from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


def login(username, password) -> tuple[bool, Response]:
    user = authenticate(
        username=username,
        password=password,
    )
    if user:
        user.save() # -> generates new token
        token = user.auth_tokens.first()
        return True, Response({'token': token.key}, status=status.HTTP_200_OK)

    return False, Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class SignUpView(APIView):
    authentication_classes = []

    def post(self, request):

        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=serializer.validated_data["username"]).exists():
            return Response({'error': 'The username is already taken'}, status=status.HTTP_409_CONFLICT)

        logged_in, login_response = login(
            serializer.validated_data.get('username'),
            serializer.validated_data.get('password')
        )
        if logged_in:
            return login_response

        user = serializer.save()
        token = user.auth_tokens.first()
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class SignInView(APIView):
    authentication_classes = []

    def post(self, request):
        _, login_response = login(
            request.data.get('ID'), 
            request.data.get('password')
        )
        return login_response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = request.user.auth_tokens.all()
        delete_all = request.data.get('all', False)
        if delete_all:
            tokens.delete()
        else:
            tokens.filter(key=request.auth.key).delete()

        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class InfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                'ID': user.username,
                'type': user.profile.id_type,
            },
            status=status.HTTP_200_OK
        )


class LatencyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            remote_host = settings.LATENCY_HOST
            start_time = time()
            response = requests.get(remote_host)
            latency_ms = int((time() - start_time) * 500)
            return Response(
                {
                    'host': remote_host,
                    'latency_ms': latency_ms,
                    'status_code': response.status_code,
                },
                status=status.HTTP_200_OK
            )

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

