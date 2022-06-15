"""Importing the libraries are need in the system..."""
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from StaffAccount.serializers import RegistrationSerializer, LoginSerializer, ChangePasswordSerializer, RoleRegistrationSerializer, RoleListSerializer
from StaffAccount.renderers import Renderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import StaffAccount, RolesStaff
from rest_framework.permissions import IsAdminUser

""" Generating tokes for the staff regstration and user login """
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

""" Admin will different roles in the system """
class RoleRegistrationView(APIView):
    renderer_classes = [Renderer]
    permission_classes = [IsAdminUser]

    def post(self, request, fromat=None):
        serializer = RoleRegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            role = serializer.save()
            role.save()
            return Response({'msg': 'New Role Has Created Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""Admin will view which roles are added into the system using this endpoint """
class RoleListView(ListAPIView):
    queryset = RolesStaff.objects.all()
    serializer_class = RoleListSerializer

""" Admin will register the staff of the society. If any other user need try register he/she not able do only admin can add  """
class RegistrationView(APIView):
    renderer_classes = [Renderer]
    permission_classes = [IsAdminUser]

    def post(self, request, fromat=None):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            staff = serializer.save()
            staff.save()

            token = get_tokens_for_user(staff)
            return Response({'access': token['access'], 'refresh': token['refresh'], 'msg': 'Registration successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

""" Staff needs login with given credentials into the system """
class LoginView(APIView):
    renderer_classes = [Renderer]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        staff = StaffAccount.objects.filter(email=email).first()
        validate_password = check_password(password=password, encoded=staff.password)
        if validate_password:
            token = get_tokens_for_user(staff)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}},
                            status=status.HTTP_404_NOT_FOUND)

""" Staff need change password on there first login into the system to access other features """
class ChangePasswordView(APIView):
    renderer_classes = [Renderer]

    def post(self, request, format=None):
        print(f"REQUEST {request.user}")
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
