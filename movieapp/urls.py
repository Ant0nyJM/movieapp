from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
                #path('accounts/login/',auth_views.LoginView.as_view(template_name='movieapp/login.html',redirect_field_name='home'),name='login'),
                path('',views.HomeView.as_view(),name='home'),
                path('search/',views.SearchView.as_view(),name='search'),
                path('accounts/',include('django.contrib.auth.urls')),
                path('accounts/signup/',views.SignupView.as_view(),name='signup'),
                path('profile/',views.UserProfileView.as_view(),name='profile'),
                path('profile/movie/',views.UserMovieView.as_view(),name='movie'),
                path('profile/movie/add/',views.MovieAddView.as_view(),name='movie_add'),
                path('movie/<int:movie_id>/',views.MovieView.as_view(),name='movie_view'),
                path('movie/<int:movie_id>/rate/',views.rate_movie,name="rate"),
                path('profile/pending/',views.PendingView.as_view(),name='pending'),
                
                
            ]