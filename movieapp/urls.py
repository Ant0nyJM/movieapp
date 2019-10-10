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
                path('profile/',views.UserProfileView.as_view(),name='profile'),
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
                path('profile/artist/delete/',views.artist_delete,name='artist_delete'),
                path('profile/artist/',views.user_artists,name="artist"),
                path('profile/artist/edit/<int:artist_id>',views.ArtistEditView.as_view(),name="artist_edit"),
                path('profile/lists/',views.lists_view,name="lists_view"),
                path('profile/list/create/',views.ListCreateView.as_view(),name="list_create"),
                path('profile/list/<int:list_id>/',views.ListView.as_view(),name="list_view"),
                path('profile/list/movie/remove/',views.list_movie_remove,name="list_movie_remove"),
                path('profile/list/delete/',views.list_delete,name="list_delete"),
                path('profile/edit/',views.ProfileEditView.as_view(),name='profile_edit'),
                
                
                path('artist-autocomplete/',views.MotionPictureAutocomplete.as_view(),name='artist-autocomplete'),
                path('director-autocomplete/',views.DirectorAutocomplete.as_view(),name='director-autocomplete'),
                path('movie-autocomplete/',views.MovieAutocomplete.as_view(),name='movie-autocomplete'),
                path('add-movie-to-list/',views.add_movie_to_list,name="add-movie-to-list"),

                
                path('jqac/',views.json_data,name="ac"),
                path('test/',views.test)
                
            ]