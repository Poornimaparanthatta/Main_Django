from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import RecruiterProfileForm
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
def recruiter_dashboard(request):
    return render(request,'recruiter_dashboard.html')

def recruiter_profile(request):
    user = request.user
    if not user.is_authenticated or not user.is_recruiter:
        return redirect('recruiter_dashboard')
    if request.method == 'POST':
        form = RecruiterProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('recruiter_dashboardd')
    else:
        form = RecruiterProfileForm(instance=user)

    return render(request, 'recruiter_profile.html', {'user': user, 'form': form})

class JobUpdateView(UpdateView):
    model = JobPost
    form_class = RecruiterProfileForm
    template_name = 'edit_job.html'
    success_url = reverse_lazy('recruiter_dashboardd')

    def get_object(self, queryset=None):
        return self.request.user

class JobDeleteView(View):
    template_name = 'delete_job.html'
    success_url = reverse_lazy('recruiter_dashboardd')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        user_profile = get_object_or_404(JobPost, username=request.user.username)

        # Delete only job-related fields, not the entire profile
        user_profile.job_title = ''
        user_profile.job_description = ''
        user_profile.required_qualifications = ''
        user_profile.desired_qualifications = ''
        user_profile.responsibilities = ''
        user_profile.application_deadline = None
        user_profile.salary_range = ''
        user_profile.location = ''
        user_profile.employment_type = ''
        user_profile.company_benefits = ''
        user_profile.how_to_apply = ''

        # Save the modified profile
        user_profile.save()

        return HttpResponseRedirect(self.success_url)


def recruiter_dashboardd(request):
    user = request.user
    if not user.is_authenticated or not user.is_recruiter:
        return redirect('index')
    user_profile = User.objects.get(username=user.username)
    return render(request, 'recruiter_data.html', {'user_profile': user_profile})

def recruiter_applications(request):
    # Assuming the logged-in user is a recruiter
    recruiter = request.user

    # Retrieve jobs posted by the recruiter
    jobs = User.objects.filter(fullname=recruiter.username)

    # Retrieve applications associated with the recruiter's jobs
    applications = JobApplication.objects.filter(job__in=jobs)

    application_details_list = []
    for application in applications:
        application_details = {
            'cover_letter': application.cover_letter,
            'resume_for_applying': application.resume_for_applying,
            'application_date': application.application_date,
            'job_title': application.job.job_title,  # Access the job title from the related job
            'applicant_name' : application.applicant.fullname,
            'status': application.status,
        }
        application_details_list.append(application_details)

    # Pass the list of application details and job titles to the template
    job_titles = [app['job_title'] for app in application_details_list]

    return render(request, 'recruiter_applications.html',
                  {'applications': application_details_list, 'job_titles': job_titles})

def update_application_status(request, applicant_name):
    applications = JobApplication.objects.filter(applicant__fullname=applicant_name)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        for application in applications:
            application.status = new_status
            application.save()

    return redirect('recruiter_applications')

