""" Libraries are import """
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from user.serializers import UserRegistrationSerializer, UserLoginSerializer, UserChangePasswordSerializer,\
    UserListSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User
from .message import UserRegstration, UserLogin, UserStatus, UserChangepassword, UserNotVerified, UserEmailNotMatch, \
    UserAlreadyVerified, UserNotGiven

""" Generating the token for the system """
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

""" User registration end point passing value and save into database  """
class UserRegistrationView(APIView):

    def post(self, request, fromat=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'access': token['access'], 'refresh': token['refresh'], 'msg': UserRegstration}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" User login view """


class UserLoginView(APIView):

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'msg':UserEmailNotMatch}, status=status.HTTP_404_NOT_FOUND)
        elif not user.is_verified:
            return Response({'msg':UserNotVerified}, status=status.HTTP_400_BAD_REQUEST)
        else:
            token = get_tokens_for_user(user)
            return Response({'access': token['access'], 'refresh': token['refresh'], 'msg': UserLogin}, status=status.HTTP_200_OK)

""" User change password endpoint """
class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': UserChangepassword}, status=status.HTTP_200_OK)

""" Admin will see user whose status is_verified is false """
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = User.objects.filter(is_verified=False)
        return queryset

""" Admin will update the status and give the permission to the user access the application """
class UserStatusUpdate(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        user_id = request.data.get('id')
        user = User.objects.filter(id=user_id).first()
        if user is None:
            return Response({'msg':UserNotGiven},status=status.HTTP_404_NOT_FOUND)
        elif user.is_verified:
            return Response({'msg':UserAlreadyVerified},status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_verified = True
            user.save()
            return Response({'msg':UserStatus}, status=status.HTTP_200_OK)
