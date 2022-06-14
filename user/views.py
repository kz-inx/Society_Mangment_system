from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView
from user.serializers import UserRegistrationSerializer, UserLoginSerializer, UserChangePasswordSerializer, UserListSerializer
from django.contrib.auth import authenticate
from user.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    # permission_classes = [IsAuthenticated]

    def post(self, request, fromat=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}},
                            status=status.HTTP_404_NOT_FOUND)
        elif not user.is_verified:
            return Response({'errors': {'non_field_errors': ['You are not verfied by the admin']}},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = User.objects.filter(is_verified=False)
        return queryset


class UserStatusUpdate(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        user_id = request.data.get('id')
        user = User.objects.filter(id=user_id).first()
        if user is None:
            return Response({'errors': {'non_field_errors': ['No user with given credentials']}},
                            status=status.HTTP_404_NOT_FOUND)
        elif user.is_verified:
            return Response({'errors': {'non_field_errors': ['User is already verified by the admin']}},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_verified=True
            user.save()
            return Response({'msg': 'Changed Status of the user...'}, status=status.HTTP_200_OK)




