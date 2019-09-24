from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

class HomeView(View):

    def get(self,request):
        return render(request,'movieapp/base.html')

class SignupView(View):
    def get(self,request):
        form = UserCreationForm()
        return render(request,'movieapp/signup.html',{'form':form})
    
    def post(self,request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return HttpResponse("Form invalid")