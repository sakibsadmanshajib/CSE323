"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Job
from .forms import AddJob, CompleteJob
from django.utils import timezone

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

def addJob(request):

    currentJobs = Job.objects.exclude(state='completed')

    if not currentJobs:
        thestate = 'serving'
    elif len(currentJobs) > 0:
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
    
    currentJobs = Job.objects.exclude(state='completed').order_by('timestamp')

    return render(request, 'app/job/currentjobs.html', {'currentJobs' : currentJobs})

def getPastJobs(request):
    
    pastJobs = Job.objects.filter(state='completed').order_by('timestamp')

    return render(request, 'app/job/pastjobs.html', {'pastJobs' : pastJobs})

def updateJobs(request):

    form = CompleteJob(request.POST)

    if form.is_valid():
        job = Job.objects.get(id=form.cleaned_data['jobID'])
        job.state = 'complete'
        job.save()
        currentJobs = Job.objects.exclude(state='completed').order_by('timestamp')
        if currentJobs is not None:
            currentJobs[0].state = 'serving'
            if currentJobs[10] is not None:
                currentJobs[10].state = 'inline'
                currentJobs[10].save()
            currentJobs[0].save()
        return redirect('getCurrentJobs')
    else:
        return redirect('getCurrentJobs')