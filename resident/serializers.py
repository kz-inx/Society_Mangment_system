""" Importing libraries """
from rest_framework import serializers
from .models import UserCompliant

""" Creating the serializers for the user can filed compliant """
class UserFileCompliantSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserCompliant
        fields = ['title', 'subject']


""" User complain can see by the admin of the system only """
class SeeCompliantSerializers(serializers.ModelSerializer):
    user_house_no = serializers.CharField(source="user.house_no", read_only=True)
    class Meta:
        model = UserCompliant
        fields = ['id','title','subject','user_house_no','status']
