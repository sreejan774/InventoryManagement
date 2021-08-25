from django.contrib import auth
from django.shortcuts import redirect, render
from authinventory import forms 
from django.contrib.auth import authenticate , login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


# Create your views here.
def signup(request):
    signupform = forms.SignUpForm()
    error = None 
    if request.method == "POST":
        signupform = forms.SignUpForm(request.POST)
        if signupform.is_valid():
            username = signupform.cleaned_data['username']
            password = signupform.cleaned_data['password']
            confirmpassword = signupform.cleaned_data['confirmPassword']

            if(password != confirmpassword):
                error = "Password Didn't Match"
            else:
                try:
                    user = User.objects.create_user(
                        username = username,
                        password = password
                    )

                    user.save()
                    auth_login(request,user)
                    return redirect('login')
                except:
                    error = "Something went wrong"
    
    context = {
        "form" : signupform,
        "error" : error
    }

    return render(request,'authinventory/signup.html',context)


def login(request):
    loginform = forms.LoginForm()
    error = None
    if request.method == 'POST':
        loginform = forms.LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']
            user = authenticate(username = username,password = password)

            if user :
                auth_login(request,user)
                return HttpResponseRedirect('/')
            else:
                error = "Invalid username or password"


    context = {
        'form' : loginform,
        'error' : error
    }
    return render(request,'authinventory/login.html',context)


def logout(request):
    auth_logout(request)
    return redirect('login')

