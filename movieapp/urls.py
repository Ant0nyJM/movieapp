from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse
urlpatterns = [
                #path('accounts/login/',auth_views.LoginView.as_view(template_name='movieapp/login.html',redirect_field_name='home'),name='login'),
                path('',views.HomeView.as_view(),name='home'),
                path('search/',views.SearchView.as_view(),name='search'),
                path('accounts/',include('django.contrib.auth.urls')),
                #path('accounts/reset/done/',auth_views.PasswordResetConfirmView.as_view(success_url=reverse('movieapp:home')),name="password_reset_confirm"),
                path('accounts/signup/',views.SignupView.as_view(),name='signup'),
                path('profile/',views.UserMovieView.as_view(),name='profile'),
                path('profile/movie/',views.UserMovieView.as_view(),name='movie'),
                path('profile/movie/edit/<int:movie_id>/',views.MovieEditView.as_view(),name="movie_edit"),
                path('profile/movie/delete/',views.movie_delete,name="movie_delete"),
                path('profile/movie/add/',views.MovieAddView.as_view(),name='movie_add'),
                path('movie/<int:movie_id>/',views.MovieView.as_view(),name='movie_view'),
                path('movie/<int:movie_id>/rate/',views.rate_movie,name="rate"),
                path('profile/pending/',views.PendingView.as_view(),name='pending'),
                path('profile/<int:movie_id>/review/',views.review_movie,name="review"),
                path('profile/reviews/',views.user_reviews,name='user_reviews'),
                path('profile/review/delete/',views.review_delete,name="review_delete"),
                path('profile/review/edit/<int:review_id>/',views.ReviewEditView.as_view(),name="review_edit"),
                path('profile/artist/add/',views.ArtistAddView.as_view(),name='artist_add'),
                path('artist/<int:artist_id>/',views.ArtistView.as_view(),name='artist_view'),


                path('artist/',views.artist_search),
                path('artist-autocomplete/',views.MotionPictureAutocomplete.as_view(),name='artist-autocomplete'),

                
                path('jqac/',views.json_data,name="ac"),
                path('test/',views.test)
                
            ]