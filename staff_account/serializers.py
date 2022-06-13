from rest_framework import serializers
from staff_account.models import StaffAccount


class StaffRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAccount
        fields = ['name', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
