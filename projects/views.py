from django.shortcuts import render


def projects(request):
    return render(request, 'projects/projects.html')


def projects(request, pk):
    return render(request, 'projects/single-project.html')
