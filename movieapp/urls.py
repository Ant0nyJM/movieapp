from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
                path('accounts/login/',auth_views.LoginView.as_view(template_name='movieapp/login.html',redirect_field_name='home'),name='login'),
                path('accounts/signup/',views.SignupView.as_view(),name='signup'),
                path('',views.HomeView.as_view(),name='home'),
                
            ]