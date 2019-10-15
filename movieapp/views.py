from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,JsonResponse
from django.views import View
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm,MovieReviewForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from . import models as my_models
from . import forms as my_forms

from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from django.core import serializers

import json

from django.utils import timezone
from .models import MotionPicture



class MotionPictureAutocomplete(View):
    def get(self,request):
        # Don't forget to filter out results depending on the visitor !
        

        qs = my_models.Artist.objects.all()
        q = request.GET.get('q','')
        print("-- ",request.GET)
        try:
            if q[0]!='':
                qs = qs.filter(name__icontains=q,artist_type="Actor")
            print(qs)
            return JsonResponse(serializers.serialize('json',qs),safe=False)
        except IndexError:
            return JsonResponse({})

        

def artist_search(request):
    form = my_forms.ArtistSearchForm()
    return render(request,'movieapp/artist-search.html',{'form':form})

def json_data(request):
    return JsonResponse([{"name":"Viola Francis",
      "image": "https://media.licdn.com/mpr/mpr/shrinknp_200_200/AAEAAQAAAAAAAASJAAAAJGMyMTUzN2EyLTExY2ItNDZiNS1hMTY1LTI4NDA2NDMwZmFkNg.jpg",
      "location":"Zanesville, OH"}],safe=False)

def test(request):
    return render(request,'movieapp/file.html')



# Create your views here.

class HomeView(View):

    def get(self,request):
        #return render(request,'movieapp/base.html')
        movies = my_models.MotionPicture.objects.filter(approved=True)
        rated_movies = movies.order_by('-rating')[:5]
        movies2 = movies.filter(release_date__gt=timezone.now(),release_date__lt=timezone.now()+timezone.timedelta(days=30))
        releasing_movies = movies2.order_by('release_date')[:5]
        return render(request,'movieapp/newhome.html',{'movies':movies,'rated_movies':rated_movies,'releasing_movies':releasing_movies})

class SignupView(View):
    def get(self,request):
        form = CustomUserCreationForm()
        return render(request,'movieapp/signup.html',{'form':form})
    
    def post(self,request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
        return render(request,'movieapp/signup.html',{'form':form})

class UserProfileView(View):
    def get(self,request):
        orig_user = User.objects.get(username=request.user.username)
        
        if orig_user.is_superuser:
            return redirect(reverse('pending'))
        else:
            movies = my_models.MotionPicture.objects.filter(user=orig_user)
            return render(request,'movieapp/movie.html',{'movies':movies})


class UserMovieView(View):
    def get(self,request):
        orig_user = User.objects.get(username=request.user.username)
        
        if orig_user.is_superuser:
            movies = my_models.MotionPicture.objects.filter(approved=True)
            return render(request,'movieapp/movie.html',{'movies':movies})
        else:
            movies = my_models.MotionPicture.objects.filter(user=orig_user)
            return render(request,'movieapp/movie.html',{'movies':movies})

class MovieAddView(View):


    def get(self,request):
        form = my_forms.MotionPictureForm()
        return render(request,'movieapp/movie_add.html',{'form':form})

    
    def post(self,request):
        form = my_forms.MotionPictureForm(request.POST,request.FILES)
        usr = form.save(commit=False)
        usr.user = User.objects.get(username=request.user.username)
        usr.save()
        movie = my_models.MotionPicture.objects.get(movie_id=usr.pk)
        try:
            director = my_models.Artist.objects.get(artist_id=request.POST.get('director-id'))
            director.movies.add(movie)
            director.save()
        except ValueError:
            pass
        ids = request.POST.getlist('artist_ids[]')
        for x in ids:
            print(x)
            artist = my_models.Artist.objects.get(artist_id=x)
            
            artist.movies.add(movie)
            artist.save()
        return redirect('movie')
        
        
        # if form.is_valid():
        #     print("form is valid**********************************************", form.user)
        #     form.save()
        #     return redirect('movie')
        # else:
        #     return HttpResponse(form.errors)
        # new_mp = my_models.MotionPicture(name=params['name'],genre=params['genre'],release_date=params['release_date'],description=params['description'],user=current_user,image=params.get('image'))
        # new_mp.save()
        # return redirect('movie')

class MovieView(View):
    def get(self,request,movie_id):
        context = {}
        movie = my_models.MotionPicture.objects.get(movie_id=movie_id)
        rating_len = len(my_models.Rate.objects.filter(movie = movie))
        reviews = my_models.Review.objects.filter(movie=movie)
        actors = movie.artist_set.filter(artist_type="Actor")
        print("------------.",actors)
        try:
            director = movie.artist_set.get(artist_type="Director")
        except my_models.Artist.DoesNotExist:
            director = None
        print("----------",director)
        if(director!=None):
            context['director']= director

        if(len(actors)!=0):
            context['actors']=actors
        reviews_len = len(reviews)
        review_form = MovieReviewForm()
        context.update({'movie':movie,'rating_len':rating_len,'review_form':review_form,'reviews':reviews,'reviews_len':reviews_len})
        print("888888",context)
        if request.user.is_authenticated:
            movs = my_models.List.objects.exclude(movies=movie)
            user_lists = movs.filter(user=request.user)
            user = User.objects.get(username=request.user.username)
            not_rated = True if len(my_models.Rate.objects.filter(user=user,movie=movie))<1 else False
            context['not_rated']=not_rated
            context['user_lists']=user_lists

            return render(request,'movieapp/movie_view.html',context)#
        else:
            return render(request,'movieapp/movie_view.html',context)


class PendingView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self,request):
        if request.user.is_superuser:

            pending = my_models.MotionPicture.objects.filter(approved=False)
            pending_art = my_models.Artist.objects.filter(approved=False)
            print(str(pending_art))
        else:
            pending = my_models.MotionPicture.objects.filter(user=request.user,approved=False)
            pending_art = my_models.Artist.objects.filter(user=request.user,approved=False)
        return render(request,'movieapp/pending.html',{'pending':pending,'pending_art':pending_art})

    def post(self,request):
        print(request.POST)
        if 'artist_id' in request.POST:
            artist = my_models.Artist.objects.get(artist_id=request.POST.get('artist_id'))
            artist.approved = True
            artist.save()
            return JsonResponse({'approved':'true','msg':'{} is approved'.format(artist.name)})
        if 'movie_id' in request.POST:
            movie = my_models.MotionPicture.objects.get(movie_id=request.POST.get('movie_id'))
            movie.approved = True
            movie.save()
            return JsonResponse({'approved':'true','msg':'{} is approved'.format(movie.name)})

class SearchView(View):
    def get(self,request):
        print("-------------",request.GET)
        q = request.GET.get('q','')
        try:
            if q[0] != '' :
                movies = my_models.MotionPicture.objects.filter(name__icontains=q,approved=True)
                artists = my_models.Artist.objects.filter(name__icontains=q,approved=True)
                genre = my_models.MotionPicture.objects.filter(genre__iexact=q,approved=True)
                return render(request,'movieapp/search.html',{'movies':movies,'artists':artists,'genre':genre})

        except IndexError:
            return redirect('home')

def rate_movie(request,movie_id):
    if request.method == "POST":
        rating = request.POST.get('rating')
        movie = my_models.MotionPicture.objects.get(movie_id=movie_id)
        user = User.objects.get(username = request.user.username)
        try:
            assert len(my_models.Rate.objects.filter(user=user,movie=movie))==0,"User already rated"
        except AssertionError:
            return redirect(reverse('movie_view',args=[movie_id]))
        
        movie_rating = my_models.Rate(rating=rating,movie=movie,user=user)
        movie_rating.save()
        movie.rating = my_models.Rate.objects.filter(movie = movie).aggregate(Avg('rating'))['rating__avg']
        movie.save()
        return redirect(reverse('movie_view',args=[movie_id]))
    else:
        return redirect('home')

def review_movie(request,movie_id):
    if request.method == "POST":
        review = request.POST.get('review')
        movie = my_models.MotionPicture.objects.get(movie_id=movie_id)
        user = User.objects.get(username = request.user.username)
        try:
            assert len(my_models.Review.objects.filter(user=user,movie=movie))==0,"User already reviewed"
        except AssertionError:
            return redirect(reverse('movie_view',args=[movie_id]))
        movie_review = my_models.Review(review=review,movie=movie,user=user)
        movie_review.save()
        return redirect(reverse('movie_view',args=[movie_id]))
    else:
        return redirect('home')

def user_reviews(request):
    user = User.objects.get(username=request.user.username)
    user_reviews = my_models.Review.objects.filter(user=user)
    print(user_reviews)
    return render(request,'movieapp/user_reviews.html',{'user_reviews':user_reviews})

def movie_delete(request):
    movie = my_models.MotionPicture.objects.get(movie_id=int(request.GET.get('movie_id')))
    movie.delete()
    return JsonResponse({'deleted':'deleted'})

class MovieEditView(View):
    def get(self,request,movie_id):
        movie = my_models.MotionPicture.objects.get(movie_id=movie_id)
        try:
            director = movie.artist_set.get(artist_type='Director')
        except my_models.Artist.DoesNotExist:
            director = None
        actors = movie.artist_set.filter(artist_type="Actor")
        form = my_forms.MotionPictureForm(instance=movie)
        context = {}
        context.update({'form':form})
        if(len(actors)!=0):
            context['actors'] = actors
        if(director!=None):
            context['director'] = director
        print("----->",context)
        return render(request,'movieapp/movie_edit.html',context)

    def post(self,request,movie_id):
        movie = my_models.MotionPicture.objects.get(movie_id=movie_id)
        if(request.FILES):
            print("=--============")
            form = my_forms.MotionPictureForm(request.POST,request.FILES)
            usr = form.save(commit=False)
        else:
            form = my_forms.MotionPictureForm(request.POST)
            usr = form.save(commit=False)
            usr.image = movie.image
        
        
        usr.user = User.objects.get(username=request.user.username)
        
        usr.movie_id = movie_id
        if(movie.approved):
            usr.approved = True
        usr.save()

        
        movie.artist_set.clear()
        try:
            director = my_models.Artist.objects.get(artist_id=request.POST.get('director-id'))
            director.movies.add(movie)
            director.save()
        except ValueError:
            pass
        ids = request.POST.getlist('artist_ids[]')
        for x in ids:
            print(x)
            artist = my_models.Artist.objects.get(artist_id=x)
            
            artist.movies.add(movie)
            artist.save()
        return redirect(reverse('movie_view',args=[movie_id]))

def review_delete(request):
    review = my_models.Review.objects.get(id=request.GET.get('review_id'))
    review.delete()
    return JsonResponse({'deleted':'deleted'})

class ReviewEditView(View):
    def get(self,request,review_id):
        review = my_models.Review.objects.get(id=review_id)
        form = my_forms.MovieReviewForm(instance=review)
        return render(request,'movieapp/review_edit.html',{'form':form})
    
    def post(self,request,review_id):
        review = my_models.Review.objects.get(id=review_id)
        review.review = request.POST.get('review')
        review.save()
        # print("----->"+str(request.user.username))
        # print("---->"+my_models.Review.objects.get(id=review_id).movie.name)
        return redirect(reverse('user_reviews'))

class ArtistAddView(View):
    def get(self,request):
        form = my_forms.ArtistForm()
        return render(request,'movieapp/artist_add.html',{'form':form})

    def post(self,request):
        form = my_forms.ArtistForm(request.POST,request.FILES)
        usr = form.save(commit=False)
        usr.user = User.objects.get(username=request.user.username)
        usr.save()
        artist_id = usr.artist_id
        return redirect(reverse('artist_view',args=[artist_id]))

class ArtistView(View):
    def get(self,request,artist_id):
        artist = my_models.Artist.objects.get(artist_id=artist_id)
        return render(request,'movieapp/artist_view.html',{'artist':artist})



def artist_delete(request):
    artist = my_models.Artist.objects.get(artist_id=int(request.GET.get('artist_id')))
    print("artost ====",artist.name)
    artist.delete()
    return JsonResponse({'deleted':'deleted'})


def user_artists(request):
    if request.user.is_superuser:
        artists = my_models.Artist.objects.all()
    else:
        artists = my_models.Artist.objects.filter(user = request.user)
    return render(request,'movieapp/artist.html',{'artists':artists})


class DirectorAutocomplete(View):
    def get(self,request):
        # Don't forget to filter out results depending on the visitor !
        

        qs = my_models.Artist.objects.all()
        q = request.GET.get('q','')
        print("-- ",request.GET)
        try:
            if q[0]!='':
                qs = qs.filter(name__icontains=q,artist_type='Director')
            print(qs)
            return JsonResponse(serializers.serialize('json',qs),safe=False)
        except IndexError:
            return JsonResponse({})

class MovieAutocomplete(View):
    def get(self,request):
        # Don't forget to filter out results depending on the visitor !
        

        qs = my_models.MotionPicture.objects.all()
        q = request.GET.get('q','')
        print("-- ",request.GET)
        try:
            if q[0]!='':
                qs = qs.filter(name__icontains=q,approved=True)
            print(qs)
            return JsonResponse(serializers.serialize('json',qs),safe=False)
        except IndexError:
            return JsonResponse({})



class ArtistEditView(View):
    def get(self,request,artist_id):
        artist = my_models.Artist.objects.get(artist_id=artist_id)
        form = my_forms.ArtistForm(instance= artist)
        return render(request,'movieapp/artist_edit.html',{'form':form})

    def post(self,request,artist_id):
        artist = my_models.Artist.objects.get(artist_id=artist_id)
        if(request.FILES):
            form = my_forms.ArtistForm(request.POST,request.FILES)
            usr = form.save(commit=False)
        else:
            form = my_forms.ArtistForm(request.POST)
            usr = form.save(commit=False)
            usr.image = artist.image
            
        usr.user = User.objects.get(username=request.user.username)
        usr.artist_id = artist_id
        usr.save()
        return redirect(reverse('artist_view',args=[artist_id]))


            
def lists_view(request):        
    user = User.objects.get(username=request.user.username)
    lists = my_models.List.objects.filter(user=user)
    return render(request,'movieapp/lists_view.html',{'lists':lists})


class ListCreateView(View):
    def get(self,request):
        form = my_forms.ListForm()
        return render(request,'movieapp/list_create.html',{'form':form})
    def post(self,request):
        print("Request parametres",str(request.POST))


        form = my_forms.ListForm(request.POST)
        usr = form.save(commit=False)
        usr.user = User.objects.get(username=request.user.username)
        usr.save()
        
        ids = request.POST.getlist('movie_ids[]')
        for x in ids:
            print(x)
            movie = my_models.MotionPicture.objects.get(movie_id=x)
            print("-------mvie id",movie.name)
            usr.movies.add(movie)
            usr.save()
        return redirect(reverse('list_view',args=[usr.id]))


class ListView(View):
    def get(self,request,list_id):
        lis = my_models.List.objects.get(id=list_id)
        return render(request,'movieapp/list_view.html',{'list':lis})


def list_movie_remove(request):
    print("params ----->",str(request.GET))
    movie = my_models.MotionPicture.objects.get(movie_id=request.GET.get('movie_id'))
    print(movie.name)
    lis = my_models.List.objects.get(id=request.GET.get('list_id'))
    lis.movies.remove(movie)
    print(lis.name)
    return JsonResponse({'deleted':'deleted'})


def list_delete(request):
    lis = my_models.List.objects.get(id=request.GET.get('list_id'))
    lis.delete()
    return JsonResponse({'deleted':'deleted'})

def add_movie_to_list(request):
    lis = my_models.List.objects.get(id=request.GET.get('list_id'))
    movie = my_models.MotionPicture.objects.get(movie_id=request.GET.get('movie_id'))
    if(len(lis.movies.filter(movie_id=movie.movie_id))==0):
        lis.movies.add(movie)
        return JsonResponse({'status':'added'})
    else:
        return JsonResponse({'status':'present'})

class ProfileEditView(View):
    def get(self,request):
        user = User.objects.get(username=request.user.username)
        form = UserChangeForm(instance=user)
        return render(request,'movieapp/profile.html',{'form':form})
    
    def post(self,request):
        form = UserChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request,'profile_edit',{'form':form})