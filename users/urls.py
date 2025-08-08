from django.urls import path
from .views import ChangePasswordView, LoginView, RegisterView,  LoginView, logout_view ,  logout_view , PasswordResetRequestView, PasswordResetConfirmView, PasswordResetConfirmView
from .views import UserDetailView


urlpatterns = [
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/logout/', logout_view, name='logout'),
    path('users/password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('users/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    path('users/me/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', UserDetailView.as_view(), name='user-profile'),
     path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]