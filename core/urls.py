"""
URL configuration for mainproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import *
from account.views import *
from job_seeker.views import *
from recruiter.views import *
urlpatterns = [
    path('registerPage/',registerPage,name='registerPage'),
    path('login/',loginPage,name='loginPage'),
    path('',index,name='index'),
    path('job_seeker_dashboard/',job_seeker_dashboard,name='job_seeker_dashboard'),
    path('recruiter_dashboard/',recruiter_dashboard,name='recruiter_dashboard'),
    path('profile/',profile,name='profile'),
    path('dashbaord/',dashboard,name='dashboard'),
    path('recruiter_profile/',recruiter_profile,name='recruiter_profile'),
    path('edit_job/', JobUpdateView.as_view(), name='edit_job'),
    path('delete_job/', JobDeleteView.as_view(), name='delete_job'),
    path('recruiter_dashboardd/',recruiter_dashboardd,name='recruiter_dashboardd'),
    path('job_listings/',job_listings,name='job_listings'),
    path('apply_for_job/<str:recruiter_name>/', apply_for_job, name='apply_for_job'),
    path('recruiter_applications/', recruiter_applications, name='recruiter_applications'),
    path('logout/',logout_view,name='logout'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('update_application_status/<str:applicant_name>/', update_application_status, name='update_application_status'),
    path('applied_jobs',applied_jobs,name='applied_jobs'),
]

