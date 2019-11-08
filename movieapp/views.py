import json
import requests
import barcode 

from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator
from django.core.files import File
from django.db.models import Avg, prefetch_related_objects
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from . import forms as my_forms
from . import models as my_models
from .forms import CustomUserCreationForm, MovieReviewForm
from .models import MotionPicture

import pdb

class MotionPictureAutocomplete(View):
    def get(self,request):
        # Don't forget to filter out results depending on the visitor !
        

        qs = my_models.Artist.objects.all()
        q = request.GET.get('q','')
        try:
            if q[0]!='':
                qs = qs.filter(name__icontains=q,artist_type="Actor",approved=True)
            return JsonResponse(serializers.serialize('json',qs),safe=False)
        except IndexError:
            return JsonResponse({})

        

def artist_search(request):
    form = my_forms.ArtistSearchForm()
    return render(request,'movieapp/artist-search.html',{'form':form})


def test(request):
    return render(request,'movieapp/file.html')


class HomeView(View):

    def get(self,request):
        #return render(request,'movieapp/base.html')
        movies_list = my_models.MotionPicture.objects.filter(approved=True).order_by('-created_date_time')
        paginator = Paginator(movies_list,6)
        page = request.GET.get('page',1)
        movies = paginator.get_page(page)
        rated_movies = movies_list.order_by('-rating')[:5]
        movies2 = movies_list.filter(release_date__gt=timezone.now(),release_date__lt=timezone.now()+timezone.timedelta(days=30))
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


class UserProfileView(LoginRequiredMixin,View):
    def get(self,request):
        orig_user = User.objects.get(username=request.user.username)
        
        if orig_user.is_superuser:
            return redirect(reverse('pending'))
        else:
           return redirect(reverse('movie'))


class UserMovieView(LoginRequiredMixin,View):
    def get(self,request):
        orig_user = User.objects.get(username=request.user.username)
        
        if orig_user.is_superuser:
            movies_list = my_models.MotionPicture.objects.filter(approved=True).order_by('-created_date_time')
        else:
            movies_list = my_models.MotionPicture.objects.filter(user=orig_user)
        paginator = Paginator(movies_list,10)
        page = request.GET.get('page',1)
        movies = paginator.get_page(page)
        return render(request,'movieapp/movie.html',{'movies':movies})

class MovieAddView(LoginRequiredMixin,View):


    def get(self,request):
        form = my_forms.MotionPictureForm()
        return render(request,'movieapp/movie_add.html',{'form':form})

    
    def post(self,request):
        form = my_forms.MotionPictureForm(request.POST,request.FILES)
        usr = form.save(commit=False)
        usr.user = User.objects.get(username=request.user.username)
        usr.movie_id = slugify(usr.name)
        usr.save()
        movie = my_models.MotionPicture.objects.get(movie_id=usr.pk)
        try:
            director = my_models.Artist.objects.get(artist_id=request.POST.get('director-id'))
            director.movies.add(movie)
            director.save()
        except (ValueError,my_models.Artist.DoesNotExist):
            pass

        ids = request.POST.getlist('artist_ids[]')
        for x in ids:
            try:
                artist = my_models.Artist.objects.get(artist_id=x)
                artist.movies.add(movie)
                artist.save()
            except my_models.Artist.DoesNotExist:
                pass
        return redirect(reverse('pending')+"?show_model=Movies")
        


class MovieView(View):
    def get(self,request,movie_id):
        context = {}
        
        movie = get_object_or_404(my_models.MotionPicture,movie_id=movie_id)
        prefetch_related_objects(movie)
        
        rating_len = movie.rate_set.all().count()
        reviews = movie.review_set.all()
        artists = movie.artist_set.all().defer('description','birthday')
        actors = artists.filter(artist_type="Actor")

        barcode = gen_or_get_barcode(request)

        if(actors.exists()):
            context['actors']=actors
            
        try:
            director = artists.get(artist_type="Director")
            context['director']= director
        except my_models.Artist.DoesNotExist:
            director = None

        reviews_len = reviews.count()
        current_user_reviewed = True if reviews_len > 0 else False

        review_form = MovieReviewForm()
        context.update({'barcode':barcode,'movie':movie,'rating_len':rating_len,'review_form':review_form,'reviews':reviews,'reviews_len':reviews_len,'current_user_reviewed':current_user_reviewed})

        if request.user.is_authenticated:
            user = request.user
            user_lists = my_models.List.objects.filter(user=user).exclude(movies=movie)
            
            
            not_rated = True if my_models.Rate.objects.filter(user=user,movie=movie).count() <1 else False
            context['not_rated']=not_rated
            context['user_lists']=user_lists

            return render(request,'movieapp/movie_view.html',context)#
        else:
            return render(request,'movieapp/movie_view.html',context)


class PendingView(LoginRequiredMixin,View):

    def get(self,request):
        

        if 'query' in request.GET:
            query = request.GET.get('query')
        
        if 'show_model' in request.GET:
            model = request.GET.get('show_model')
            if model == 'Artists':
                try:
                    pending_art_list = my_models.Artist.objects.filter(approved=False,name__icontains=query).order_by('-created_date_time')
                except NameError:
                    pending_art_list = my_models.Artist.objects.filter(approved=False).order_by('-created_date_time')
                if not request.user.is_superuser:
                    pending_art_list = pending_art_list.filter(user=request.user)
                paginator = Paginator(pending_art_list,5)
                page = request.GET.get('page',1)
                pending_art = paginator.get_page(page)
                return render(request,'movieapp/pending_artists.html',{'pending_art':pending_art,'selected':model})
                
            if model == 'Movies':
                try:
                    pending_list = my_models.MotionPicture.objects.filter(approved=False,name__icontains=query).order_by('-created_date_time')
                except NameError:
                    pending_list = my_models.MotionPicture.objects.filter(approved=False).order_by('-created_date_time')
                if not request.user.is_superuser:
                    pending_list = pending_list.filter(user=request.user)
                paginator = Paginator(pending_list,5)
                page = request.GET.get('page',1)
                pending = paginator.get_page(page)
                return render(request,'movieapp/pending_movies.html',{'pending':pending,'selected':model})
        else:
            try:
                pending_list = my_models.MotionPicture.objects.filter(approved=False,name__icontains=query).order_by('-created_date_time')
            except NameError:
                pending_list = my_models.MotionPicture.objects.filter(approved=False).order_by('-created_date_time')
            if not request.user.is_superuser:
                pending_list = pending_list.filter(user=request.user)
            paginator = Paginator(pending_list,5)
            page = request.GET.get('page',1)
            pending = paginator.get_page(page)
            return render(request,'movieapp/pending_movies.html',{'pending':pending})

    def post(self,request):
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
        q = request.GET.get('q','')
        page = request.GET.get('page',1)
        model = request.GET.get('model','')

        # try:
        if q != '' :
            context = {'q_value':q}
            if model == '':
                movies_list = my_models.MotionPicture.objects.filter(approved=True,name__icontains=q)
                if movies_list.exists():
                    paginator = Paginator(movies_list,5)
                    movies = paginator.get_page(page)
                    context.update({'movies':movies})
                else:
                    artists_list = my_models.Artist.objects.filter(approved=True,name__icontains=q)
                    if artists_list.exists():
                        paginator = Paginator(artists_list,5)
                        artists = paginator.get_page(page)
                        context.update({'artists':artists})

            if model=='Movies':
                movies_list = my_models.MotionPicture.objects.filter(approved=True,name__icontains=q)
                
                if movies_list.exists():
                    paginator = Paginator(movies_list,5)
                    movies = paginator.get_page(page)

                    context.update({'movies':movies})

            if model=='Artists':

                artists_list = my_models.Artist.objects.filter(approved=True,name__icontains=q)

                if artists_list.exists():
                    paginator = Paginator(artists_list,5)
                    artists = paginator.get_page(page)
                    context.update({'artists':artists})

            # except IndexError:

            #     movies_list = my_models.MotionPicture.objects.filter(approved=True,name__icontains=q[0])
            #     if movies_lsit.exists():
            #         context.update({'movies':movies})
            

            
            return render(request,'movieapp/search.html',context)

        # except IndexError:
        #     return redirect('home')


@login_required
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

@login_required
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

@login_required
def user_reviews(request):
    user = request.user
    user_reviews = my_models.Review.objects.filter(user=user).order_by('-created_date_time')
    return render(request,'movieapp/user_reviews.html',{'user_reviews':user_reviews})

@login_required
def movie_delete(request):
    movie = my_models.MotionPicture.objects.get(movie_id=request.GET.get('movie_id'))
    movie.delete()
    return JsonResponse({'deleted':'deleted'})

@method_decorator(login_required,name='dispatch')
class MovieEditView(View):
    def get(self,request,movie_id):

        movie = get_object_or_404(my_models.MotionPicture,movie_id=movie_id)
        if movie.user==request.user or request.user.is_superuser:
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
            return render(request,'movieapp/movie_edit.html',context)
        else:
            return redirect(reverse('movie_view',args=[movie_id]))

    def post(self,request,movie_id):
        movie = my_models.MotionPicture.objects.get(movie_id=movie_id)
        if(request.FILES):
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
        usr.created_date_time = movie.created_date_time
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
            artist = my_models.Artist.objects.get(artist_id=x)
            
            artist.movies.add(movie)
            artist.save()
        return redirect(reverse('movie_view',args=[movie_id]))


@login_required
def review_delete(request):
    review = my_models.Review.objects.get(id=request.GET.get('review_id'))
    review.delete()
    return JsonResponse({'deleted':'deleted'})
    # return HttpResponse("yes")


class ReviewEditView(LoginRequiredMixin,View):
    def get(self,request,review_id):
        review = get_object_or_404(my_models.Review,id=review_id)
        form = my_forms.MovieReviewForm(instance=review)
        return render(request,'movieapp/review_edit.html',{'form':form})
    
    def post(self,request,review_id):
        review = my_models.Review.objects.get(id=review_id)
        review.review = request.POST.get('review')
        review.save()
        return redirect(reverse('user_reviews'))


class ArtistAddView(LoginRequiredMixin,View):
    def get(self,request):
        form = my_forms.ArtistForm()
        return render(request,'movieapp/artist_add.html',{'form':form})

    def post(self,request):
        form = my_forms.ArtistForm(request.POST,request.FILES)
        usr = form.save(commit=False)
        usr.user = User.objects.get(username=request.user.username)
        usr.artist_id = slugify(usr.name)
        usr.save()
        return redirect(reverse('pending')+"?show_model=Artists")

class ArtistView(View):
    def get(self,request,artist_id):
        artist = get_object_or_404(my_models.Artist,artist_id=artist_id)
        return render(request,'movieapp/artist_view2.html',{'artist':artist})


@login_required
def artist_delete(request):
    artist = my_models.Artist.objects.get(artist_id=request.GET.get('artist_id'))
    artist.delete()
    return JsonResponse({'deleted':'deleted'})


@login_required
def user_artists(request):
    if request.user.is_superuser:
        artists_list = my_models.Artist.objects.filter(approved=True).order_by('-created_date_time')
    else:
        artists_list = my_models.Artist.objects.filter(user = request.user).order_by('-created_date_time')
    paginator = Paginator(artists_list,10)
    page = request.GET.get('page',1)
    artists = paginator.get_page(page)
    return render(request,'movieapp/artist.html',{'artists':artists})


class DirectorAutocomplete(View):
    def get(self,request):        

        qs = my_models.Artist.objects.all()
        q = request.GET.get('q','')
        try:
            if q[0]!='':
                qs = qs.filter(name__icontains=q,artist_type='Director',approved=True)
            return JsonResponse(serializers.serialize('json',qs),safe=False)
        except IndexError:
            return JsonResponse({})


class MovieAutocomplete(View):
    def get(self,request):        

        qs = my_models.MotionPicture.objects.all()
        q = request.GET.get('q','')
        try:
            if q[0]!='':
                qs = qs.filter(name__icontains=q,approved=True)
            return JsonResponse(serializers.serialize('json',qs),safe=False)
        except IndexError:
            return JsonResponse({})


class ArtistEditView(LoginRequiredMixin,View):
    def get(self,request,artist_id):

        artist = get_object_or_404(my_models.Artist,artist_id=artist_id)
        if artist.user == request.user or request.user.is_superuser:
            form = my_forms.ArtistEditForm(instance= artist)
            return render(request,'movieapp/artist_edit.html',{'form':form})
        else:
            return redirect(reverse('artist_view',args=[artist_id]))


    def post(self,request,artist_id):
        artist = my_models.Artist.objects.get(artist_id=artist_id)
        
        try:
            if(request.FILES):
                form = my_forms.ArtistEditForm(request.POST,request.FILES)
                if form.is_valid():
                    usr = form.save(commit=False)
                else:
                    return render(request,'movieapp/artist_edit.html',{'form':form})
            else:
                form = my_forms.ArtistEditForm(request.POST)
                if form.is_valid():
                    usr = form.save(commit=False)
                    usr.image = artist.image
                else:
                    return render(request,'movieapp/artist_edit.html',{'form':form})

            
            usr.artist_type = artist.artist_type
            usr.user = User.objects.get(username=request.user.username)
            usr.artist_id = artist_id
            if(artist.approved == True):
                usr.approved = True
            usr.created_date_time = artist.created_date_time
            usr.save()
            return redirect(reverse('artist_view',args=[artist_id]))
        except ValueError:
            return render(request,'movieapp/artist_edit.html',{'form':form})
        


@login_required            
def lists_view(request):        
    user = User.objects.get(username=request.user.username)
    lists = my_models.List.objects.filter(user=user)
    return render(request,'movieapp/lists_view.html',{'lists':lists})


class ListCreateView(LoginRequiredMixin,View):
    def get(self,request):
        form = my_forms.ListForm()
        return render(request,'movieapp/list_create.html',{'form':form})
    def post(self,request):


        form = my_forms.ListForm(request.POST)
        usr = form.save(commit=False)
        usr.user = User.objects.get(username=request.user.username)
        usr.save()
        
        ids = request.POST.getlist('movie_ids[]')
        for x in ids:
            movie = my_models.MotionPicture.objects.get(movie_id=x)
            usr.movies.add(movie)
            usr.save()
        return redirect(reverse('list_view',args=[usr.id]))


class ListView(LoginRequiredMixin,View):
    def get(self,request,list_id):
        lis = get_object_or_404(my_models.List.objects.select_related(),id=list_id)
        return render(request,'movieapp/list_view.html',{'list':lis})


@login_required
def list_movie_remove(request):
    movie = my_models.MotionPicture.objects.get(movie_id=request.GET.get('movie_id'))
    lis = my_models.List.objects.get(id=request.GET.get('list_id'))
    lis.movies.remove(movie)
    return JsonResponse({'deleted':'deleted'})

@login_required
def list_delete(request):
    lis = my_models.List.objects.get(id=request.GET.get('list_id'))
    lis.delete()
    return JsonResponse({'deleted':'deleted'})

@login_required
def add_movie_to_list(request):
    lis = my_models.List.objects.get(id=request.GET.get('list_id'))
    movie = my_models.MotionPicture.objects.get(movie_id=request.GET.get('movie_id'))
    if(len(lis.movies.filter(movie_id=movie.movie_id))==0):
        lis.movies.add(movie)
        return JsonResponse({'status':'added'})
    else:
        return JsonResponse({'status':'present'})


class ProfileEditView(LoginRequiredMixin,View):
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


def gen_or_get_barcode(request):

    requesting_url = request.META['HTTP_REFERER']

    user_email = request.POST.get('share-email')
    # print("requetsing url ------------",requesting_url)
    code128 = barcode.get_barcode_class('code128')

    try:
        barcode_obj = my_models.Barcode.objects.get(long_url=requesting_url)
        if(not barcode_obj.short_url ):
            short_barcode_request = json.loads(shorten_url(requesting_url))
            if(short_barcode_request['status'] == 'ok'):
                barcode_obj.short_url = short_barcode_request['link']
                barcode_obj.save()
    except my_models.Barcode.DoesNotExist:

        barcode_obj = my_models.Barcode(long_url=requesting_url)

        short_barcode_request = json.loads(shorten_url(requesting_url))
        # print("-----------",str(short_barcode_request))
        if(short_barcode_request['status'] == 'ok'):
            barcode_obj.short_url = short_barcode_request['link']
        
        barcode_obj.save()
        
    if not barcode_obj.image and barcode_obj.short_url :
        # print("no image but shorturl exists")
            
        barcode_img = code128(barcode_obj.short_url)
        barcode_img.save('barcode')

        filename = 'barcode_'+barcode_obj.short_url.split('/')[1]+".svg"
        barcode_obj.image.save(filename,File(open('barcode.svg')))
    

    return barcode_obj

def shorten_url(url):

    # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^",url)

    linkRequest = {
        "destination": url , 
        # "destination" : "https://barcodemoviedb.herokuapp.com/movie/baby/",
        "domain": { "fullName": "rebrand.ly" }
    }

    requestHeaders = {
    "Content-type": "application/json",
    "apikey": "2530603f8d76454fa2c3eaaa19d59f17",
    }
    try:
        response = requests.post("https://api.rebrandly.com/v1/links", 
            data = json.dumps(linkRequest),
            headers=requestHeaders)
    except requests.exceptions.ConnectionError:
        response.status_code = "Connection Error"

    # print("**************",str(response.text))
    if (response.status_code == requests.codes.ok):
        link = response.json()
        return json.dumps({'status':'ok','link':link['shortUrl']})
    else:
        return json.dumps({'status':'fail'})