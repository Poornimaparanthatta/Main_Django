from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from account.models import User
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test


from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request,'index.html')

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    job_seekers = User.objects.filter(usertype='Job Seeker')
    recruiters = User.objects.filter(usertype='Recruiter')

    context = {'job_seekers': job_seekers, 'recruiters': recruiters}
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete_recruiter':
            recruiter_username = request.POST.get('recruiter_username')
            recruiter = get_object_or_404(User, username=recruiter_username)
            recruiter.delete()

    return render(request, 'admin_dashboard.html', context)

def dashboard(request):
    user = request.user
    if not user.is_authenticated or not user.is_job_seeker:
        return redirect('index')
    user_profile = User.objects.get(username=user.username)
    return render(request, 'dashboard.html', {'user_profile': user_profile})