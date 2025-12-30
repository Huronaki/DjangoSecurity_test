from django.urls import path
from .views import index, register, profile, edit_profile
from django.contrib.auth import views as auth_views
from .views import export_profile_csv



urlpatterns = [
    path('', index),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('export/', export_profile_csv, name='export_csv'),
]
