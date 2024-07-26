from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . forms import LoginForm

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('registration/',views.UserRegistrationView.as_view(), name='reg'),
    path('prediction/', views.image_upload_view, name='image_upload'),
    path('output/<str:rs>/', views.output, name="output"),
    path('successfully/',views.success, name = 'successfully'),
    path('logout/',views.logout_form, name = 'logout'),
]