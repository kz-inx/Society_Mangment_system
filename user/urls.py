from django.urls import path, include
from user.views import UserRegistrationView,UserLoginView
urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
]
