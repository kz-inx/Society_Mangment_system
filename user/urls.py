from django.urls import path, include
from user.views import UserRegistrationView,UserLoginView, UserChangePasswordView, UserListView, UserStatusUpdate, PasswordResetView, PasswordResetConfirm
urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('changepassword/', UserChangePasswordView.as_view()),
    path('userlist/', UserListView.as_view()),
    path('userstatus/', UserStatusUpdate.as_view()),
    path('password_reset/',PasswordResetView.as_view()),
    path('Password-reset/confirm/', PasswordResetConfirm.as_view())


]
