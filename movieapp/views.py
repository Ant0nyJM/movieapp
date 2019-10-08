from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,JsonResponse
from django.views import View
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm,MovieReviewForm
from django.contrib.auth.models import User
from . import models as my_models
from . import forms as my_forms

from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from django.core import serializers

import json


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
        releasing_movies = movies.order_by('release_date')[:5]
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
        if request.user.is_superuser:
            return render(request,'movieapp/admin_profile.html')
        else:
            return render(request,'movieapp/user_profile2.html')


class UserMovieView(View):
    def get(self,request):
        orig_user = User.objects.get(username=request.user.username)
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
        director = my_models.Artist.objects.get(artist_id=request.POST.get('director-id'))
        director.movies.add(movie)
        director.save()
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
            user = User.objects.get(username=request.user.username)
            not_rated = True if len(my_models.Rate.objects.filter(user=user,movie=movie))<1 else False
            context['not_rated']=not_rated

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
        else:
            pending = my_models.MotionPicture.objects.filter(user=request.user,approved=False)
        return render(request,'movieapp/pending.html',{'pending':pending})

    def post(self,request):
        print(request.POST)
        print('------------------------------',request.POST.get('movie_id'))
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
                artists = my_models.Artist.objects.filter(name__icontains=q)
                genre = my_models.MotionPicture.objects.filter(genre__icontains=q,approved=True)
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
        if(request.FILES):
            form = my_forms.MotionPictureForm(request.POST,request.FILES)
        else:
            form = my_forms.MotionPictureForm(request.POST)
        
        usr = form.save(commit=False)
        usr.user = User.objects.get(username=request.user.username)
        usr.movie_id = movie_id
        usr.save()

        movie = my_models.MotionPicture.objects.get(movie_id=movie_id)
        movie.artist_set.clear()
        director = my_models.Artist.objects.get(artist_id=request.POST.get('director-id'))
        director.movies.add(movie)
        director.save()
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



class ArtistEditView(View):
    def get(self,request,artist_id):
        artist = my_models.Artist.objects.get(artist_id=artist_id)
        form = my_forms.ArtistForm(instance= artist)
        return render(request,'movieapp/artist_edit.html',{'form':form})

    def post(self,request,artist_id):
        form = my_forms.ArtistForm(request.POST,request.FILES)
        usr = form.save(commit=False)
        usr.user = User.objects.get(username=request.user.username)
        usr.artist_id = artist_id
        usr.save()
        return redirect(reverse('artist_view',args=[artist_id]))


            
        
