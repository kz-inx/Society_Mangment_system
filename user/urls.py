from django.urls import path, include
from user.views import UserRegistrationView,UserLoginView, UserChangePasswordView, UserListView, UserStatusUpdate
urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('userlist/', UserListView.as_view()),
    path('userstatus/', UserStatusUpdate.as_view())

]
