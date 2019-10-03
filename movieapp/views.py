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



# Create your views here.

class HomeView(View):

    def get(self,request):
        #return render(request,'movieapp/base.html')
        movies = my_models.MotionPicture.objects.filter(approved=True)
        return render(request,'movieapp/newhome.html',{'movies':movies})

class SignupView(View):
    def get(self,request):
        form = CustomUserCreationForm()
        return render(request,'movieapp/signup.html',{'form':form})
    
    def post(self,request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return HttpResponse("Form invalid")

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
        movie = my_models.MotionPicture.objects.get(movie_id=movie_id)
        rating = my_models.Rate.objects.filter(movie = movie).aggregate(Avg('rating'))
        rating_len = len(my_models.Rate.objects.filter(movie = movie))
        reviews = my_models.Review.objects.filter(movie=movie)
        reviews_len = len(reviews)
        review_form = MovieReviewForm()
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            not_rated = True if len(my_models.Rate.objects.filter(user=user,movie=movie))<1 else False
            return render(request,'movieapp/movie_view.html',{'movie':movie,'rating':rating,'rating_len':rating_len,'not_rated':not_rated,'review_form':review_form,'reviews':reviews,'reviews_len':reviews_len})
        else:
            return render(request,'movieapp/movie_view.html',{'movie':movie,'rating':rating,'rating_len':rating_len,'review_form':review_form,'reviews':reviews,'reviews_len':reviews_len})


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
                movies = my_models.MotionPicture.objects.filter(name__contains=q,approved=True)
                return render(request,'movieapp/search.html',{'movies':movies})

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
        form = my_forms.MotionPictureForm(instance=movie)
        return render(request,'movieapp/movie_edit.html',{'form':form})
    def post(self,request,movie_id):
        form = my_forms.MotionPictureForm(request.POST,request.FILES)
        usr = form.save(commit=False)
        usr.user = User.objects.get(username=request.user.username)
        usr.movie_id = movie_id
        usr.save()
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



            
        
