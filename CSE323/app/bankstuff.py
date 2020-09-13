from .models import Job

def isInsideBank(jobx):
    first10Jobs = Job.objects.filter(state='inline').order_by('timestamp')

    if jobx in first10Jobs:
        return True
    else:
        return False

def isBeingServed(jobx):
    servingJobs = Job.objects.filter(state='serving').order_by('timestamp')

    if jobx in servingJobs:
        return True
    else:
        return False

def isWaiting(jobx):
    after10Jobs = Job.objects.filter(state='waiting').order_by('timestamp')

    if jobx in after10Jobs:
        return True
    else:
        return False