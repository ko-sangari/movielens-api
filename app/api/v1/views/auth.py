from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from app.api.v1.serializers.auth import UserLoginSerializer


from rest_framework_simplejwt.views import TokenRefreshView


class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description="POST api/v1/token/refresh/ - Refresh JWT token.",
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@swagger_auto_schema(
    method="post",
    operation_description="Register a new user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["username", "password"],
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="Username"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Password"
            ),
        },
    ),
    responses={
        200: openapi.Response("User successfully registered"),
        400: openapi.Response("Error: Bad Request"),
    },
)
@api_view(["POST"])
def register_user(request):
    try:
        username = request.data["username"]
        password = request.data["password"]
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "token": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )
    except KeyError:
        return Response(
            {"error": "Username and password required"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@swagger_auto_schema(
    method="post",
    operation_description="Login a user and return access and refresh JWT tokens",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["username", "password"],
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="Username"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Password"
            ),
        },
    ),
    responses={
        200: openapi.Response(
            description="Successful Login",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "refresh": openapi.Schema(
                        type=openapi.TYPE_STRING, description="JWT Refresh Token"
                    ),
                    "access": openapi.Schema(
                        type=openapi.TYPE_STRING, description="JWT Access Token"
                    ),
                },
            ),
        ),
        401: openapi.Response("Error: Unauthorized - Invalid credentials"),
    },
)
@api_view(["POST"])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "token": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
