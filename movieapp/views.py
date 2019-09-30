from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,JsonResponse
from django.views import View
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from . import models as my_models
from . import forms as my_forms

from django.views.decorators.csrf import csrf_exempt
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
        return render(request,'movieapp/movie_view.html',{'movie':movie})


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
    return HttpResponse("Rated Movie")
            
        
