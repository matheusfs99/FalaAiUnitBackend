from django.db import transaction
from django.contrib.auth import authenticate

from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ("create", "login"):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            return super().create(request, *args, **kwargs)

    @action(methods=("post",), detail=False, url_path="login")
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "id": user.id,
                    "token": str(token)
                },
                status=status.HTTP_200_OK
            )

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=("post",), detail=False, url_path="logout")
    def logout(self, request):
        try:
            request.user.auth_token.delete()
            return Response({
                "logout": True},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=('get',))
    def search_by_email(self, request):
        email = request.query_params.get('email', None)
        if email is not None:
            try:
                user = User.objects.get(email=email)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"detail": "Email parameter is required."},
            status=status.HTTP_400_BAD_REQUEST
        )