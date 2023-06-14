from django.urls import path
from users.views import SignUpView, LoginView, PasswordChangeView
urlpatterns = [
    path('signup/',SignUpView.as_view()),
    path('login/',LoginView.as_view()),
    path('password_change/',PasswordChangeView.as_view()),
]