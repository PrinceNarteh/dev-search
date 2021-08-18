from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from projects.forms import ProjectForm
from projects.models import Project
from users.models import Profile


def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects/projects.html', {'projects': projects})


def project(request, pk: str):
    project = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'project': project})


@login_required(login_url='login')
def createProject(request):
    profile: Profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project: Project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile: Profile = request.user.profile
    project: Project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile: Profile = request.user.profile
    project: Project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'projects/delete_object.html', context)
