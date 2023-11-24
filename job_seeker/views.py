from django.shortcuts import render, redirect
from .forms import JobApplicationForm
from django.contrib.auth import authenticate, login,logout
from account.models import User
from recruiter.models import JobPost
from job_seeker.models import JobApplication
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
def job_seeker_dashboard(request):
    return render(request,'job_seeker_dashboard.html')

def job_listings(request):

    # Retrieve all jobs posted by recruiters
    # jobs = JobPost.objects.exclude(job_title__isnull=True,id__isnull=True).exclude(usertype='Job Seeker')
    jobs = JobPost.objects.exclude(job_title__isnull=True,id__isnull=True)

    keyword = request.GET.get('keyword', '')
    location = request.GET.get('location', '')
    industry = request.GET.get('industry', '')

    # Filter jobs based on search parameters
    if keyword:
        jobs = jobs.filter(
            Q(fullname__icontains=keyword) |
            Q(job_title__icontains=keyword) |
            Q(job_description__icontains=keyword) |
            Q(required_qualifications__icontains=keyword) |
            Q(desired_qualifications__icontains=keyword) |
            Q(responsibilities__icontains=keyword)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    jobs = jobs.exclude(job_title=None, job_description=None, required_qualifications=None, location=None)



        # Sorting - Default to sorting by application_deadline
    sort_by = request.GET.get('sort_by', 'application_deadline')  # Use '-' to indicate descending order
    if sort_by not in ['application_deadline']:
        sort_by = 'application_deadline'

    jobs = jobs.order_by(sort_by)

    job_details = []
    for job in jobs:
        job_details.append({
            'recruiter_name': job.fullname,
            'job_title': job.job_title,
            'job_description': job.job_description,
            'required_qualifications': job.required_qualifications,
            'desired_qualifications' : job.desired_qualifications,
            'responsibilities' : job.responsibilities,
            'application_deadline' : job.application_deadline,
            'salary_range' : job.salary_range,
            'location': job.location,
            'company_benefits':job.company_benefits,
            'how_to_apply':job.how_to_apply,
            'employment_type': job.employment_type,
        })

    return render(request, 'job_listings.html', {'job_details': job_details})


def apply_for_job(request, recruiter_name):
    job = User.objects.get(fullname=recruiter_name)
    existing_application = JobApplication.objects.filter(job=job, applicant=request.user).first()

    if existing_application:
        return render(request, 'already_applied.html', {'job': job, 'existing_application': existing_application})

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('applied_jobs')  # Redirect to job listings or a thank you page
    else:
        form = JobApplicationForm()

    return render(request, 'apply_for_job.html', {'form': form, 'job': job})

def applied_jobs(request):
    # Assuming the logged-in user is a job seeker
    job_seeker = request.user

    # Retrieve applications submitted by the job seeker
    applications = JobApplication.objects.filter(applicant=job_seeker)

    applied_jobs_list = []
    for application in applications:
        applied_job_details = {
            'company_name': application.job.fullname,  # Assuming 'fullname' is the company name
            'job_title': application.job.job_title,
            'application_status': application.status,
        }
        applied_jobs_list.append(applied_job_details)

    return render(request, 'applied_jobs.html', {'applied_jobs_list': applied_jobs_list})