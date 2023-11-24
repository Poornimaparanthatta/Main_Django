from django.shortcuts import render, redirect
from .forms import registerForm,loginForm,UserProfileForm
from django.contrib.auth import authenticate, login,logout
from .models import User
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test


from django.contrib.auth.decorators import login_required

def registerPage(request):
    register_form = registerForm()
    
    if request.method == 'POST':
        register_form = registerForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect('loginPage')
        
    return render(request, 'register.html', {'register_form': register_form})

def loginPage(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            print("============form.is_valid=========================")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print("username", username)
            print("password", password)
            user_obj = User.objects.filter(username=username, password=password)
            print("user_obj", user_obj)
            user = authenticate(request, username=username, password=password)
            print("user", user)
            if user:
                login(request, user)
                if user.is_job_seeker:
                    return redirect('job_seeker_dashboard')
                elif user.is_recruiter:
                    return redirect('recruiter_dashboard')
                elif user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    # Handle the case where the user type in the form does not match the user's actual type
                    return redirect('index')

            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid login credentials'})
        else:
            print("=========invalid-form===============")
    else:
        print("=========invalid-method===============")
        form = loginForm()

    return render(request, 'login.html', {'form': form})

def profile(request):
    user = request.user
    if not user.is_authenticated or not user.is_job_seeker:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'profile.html', {'user': user, 'form': form})

def index(request):
    return render(request,'index.html')

def dashboard(request):
    user = request.user
    if not user.is_authenticated or not user.is_job_seeker:
        return redirect('index')
    user_profile = User.objects.get(username=user.username)
    return render(request, 'dashboard.html', {'user_profile': user_profile})

def logout_view(request):
    logout(request)
    return redirect('loginPage')