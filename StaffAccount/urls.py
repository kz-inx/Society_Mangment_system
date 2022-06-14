from django.urls import path
from StaffAccount.views import RegistrationView, LoginView, ChangePasswordView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('changepassword/', ChangePasswordView.as_view())
]