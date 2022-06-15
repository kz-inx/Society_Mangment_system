from django.urls import path
from StaffAccount.views import RegistrationView, LoginView, ChangePasswordView, RoleRegistrationView, RoleListView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('changepassword/', ChangePasswordView.as_view()),
    path('role/register/', RoleRegistrationView.as_view()),
    path('role/list/', RoleListView.as_view())

]