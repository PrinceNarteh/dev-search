from django.shortcuts import render
from .models import Profile


def profiles(request):
    profiles = Profile.objects.all()
    print(profiles)
    return render(request, 'users/profiles.html', { "profiles" : profiles})
