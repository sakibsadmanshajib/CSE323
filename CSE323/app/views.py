"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Job
from .forms import AddJob, CompleteJob
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

@login_required
def addJob(request):

    currentJobs = Job.objects.exclude(state='completed')

    if not currentJobs:
        thestate = 'serving'
    elif len(currentJobs) > 0 and len(currentJobs) < 10:
        thestate = 'inline'
    else:
        thestate = 'waiting'
    if request.method == 'POST':
        form = AddJob(request.POST)
        if form.is_valid():
            job = Job(
                user = form.cleaned_data['user'],
                userID = form.cleaned_data['userID'],
                job = form.cleaned_data['job'],
                timestamp = timezone.now(),
                priority = form.cleaned_data['priority'],
                state = thestate,
            )
            job.save()

            return redirect('getCurrentJobs')

        else:
            return redirect('getCurrentJobs')
    
    else:
        form = AddJob()
        return render(request, 'app/job/add.html', {'form': form})

def getCurrentJobs(request):
    
    servingJobs = Job.objects.filter(state='serving').order_by('timestamp')
    inLineJobs = Job.objects.filter(state='inline').order_by('timestamp')
    waitingJobs = Job.objects.filter(state='waiting').order_by('timestamp')
    currentJobs = Job.objects.exclude(state='completed').order_by('timestamp')

    return render(request, 'app/job/currentjobs.html', {'servingJobs' : servingJobs, 'inLineJobs' : inLineJobs, 'waitingJobs' : waitingJobs, 'currentJobs': currentJobs})

@user_passes_test(lambda u: u.is_superuser)
def getPastJobs(request):
    
    pastJobs = Job.objects.filter(state='completed').order_by('timestamp')

    return render(request, 'app/job/pastjobs.html', {'pastJobs' : pastJobs})

@user_passes_test(lambda u: u.is_superuser)
def updateJobs(request):

    form = CompleteJob(request.POST)

    if form.is_valid():
        job = Job.objects.get(id=form.cleaned_data['jobID'])
        job.state = 'completed'
        job.save()
        currentJobs = Job.objects.exclude(state='completed').order_by('timestamp')
        if currentJobs:
            currentJobs[0].state = 'serving'
            currentJobs[0].save()
            if len(currentJobs)-1 > 0 and currentJobs[len(currentJobs)-1]:
                currentJobs[len(currentJobs)-1].state = 'inline'
                currentJobs[len(currentJobs)-1].save()
        return redirect('getCurrentJobs')
    else:
        return redirect('getCurrentJobs')