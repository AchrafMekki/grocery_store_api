
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializer import SignUpSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username  # that would be envrypted into the token
        token["password"] = user.password
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


"""
curl -X POST http://localhost:8000/api/v1/customer/token/
curl -H "Content-Type: application/json" http://localhost:8000/api/v1/customer/token/
curl -d '{"username": "admin", "password": "admin"}' http://localhost:8000/api/v1/customer/token/
"""
@api_view(["POST"])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data["email"]).exists():
            user = User.objects.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                username=data["email"],
                password=make_password(data["password"]),
            )
            return Response({"detail": "User created"}, status=status.HTTP_201_CREATED)

        else:
            return Response(
                {"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

    else:
        return Response(user.errors)
