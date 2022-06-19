""" Importing Libraries """
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import AdminNotifcationSerializers, AdminNotifcationParticularSerializers
from .models import Notifcation
from .message import SentNotifcation, SentParticularUser
from django.db.models import Q
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.core.mail import send_mail
from user.models import User

""" Send Notifications to all user in the system """
class AdminSentNotifcationAll(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AdminNotifcationSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            notifcation = serializer.save()
            user_query = User.objects.all()
            email_list = user_query.values_list('email', flat=True)
            print(email_list)
            send_mail(
                notifcation.title,
                notifcation.message,
                'djangoblogkunal@gmail.com',
                email_list,
                fail_silently=False,
            )
            return Response({'status':'Successfully','msg': SentNotifcation}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

""" Send notifications to particular user in the system"""
class AdminSentNotifcationParticular(APIView):
    permission_classes = [IsAdminUser]

    def post(self,request):
        serializer = AdminNotifcationParticularSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            notifcation = serializer.save()
            house_no = notifcation.house_no
            user = User.objects.filter(house_no=house_no)
            ids = user.values_list('email', flat=True)
            send_mail(
                notifcation.title,
                notifcation.message,
                'djangoblogkunal@gmail.com',
                ids,
                fail_silently=False,
            )
            return Response({'status':'Successfully','msg': SentParticularUser}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" See notification by the user on there particular endpoint """
class SeeNotifcation(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Notifcation.objects.all()
    serializer_class = AdminNotifcationSerializers

    def get_queryset(self):
        queryset = Notifcation.objects.filter(Q(house_no=self.request.user.house_no) | Q(house_no="")).order_by('-created_at')
        return queryset
