from django.urls import path, include
from staff_account.views import StaffRegistartaion

urlpatterns = [
    path('register/', StaffRegistartaion.as_view()),
]