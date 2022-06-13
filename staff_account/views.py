from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from staff_account.serializers import StaffRegistrationSerializer
from django.contrib.auth import authenticate
from staff_account.renderers import StaffRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.

class StaffRegistartaion(APIView):
    renderer_classes = [StaffRenderer]

    def post(self, request, fromat=None):
        serializer = StaffRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
