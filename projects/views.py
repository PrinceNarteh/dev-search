from django.shortcuts import render
from .models import Project


def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects/projects.html', {'projects': projects})


def project(request, pk: str):
    project = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'project': project})
