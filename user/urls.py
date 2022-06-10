from django.urls import path, include
from user.views import UserRegistrationView,UserLoginView, UserChangePasswordView
urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
]
