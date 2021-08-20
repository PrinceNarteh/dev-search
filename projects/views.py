from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, render

from projects.forms import ProjectForm
from projects.models import Project
from projects.utils import search_projects
from users.models import Profile


def projects(request):
    projects, search_query = search_projects(request)
    
    page = request.GET.get('page')
    results_per_page = 3
    paginator = Paginator(projects, results_per_page)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    context = {'projects': projects, "search_query": search_query}
    return render(request, 'projects/projects.html', context)


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
            messages.success('Project created successfully!')
            return redirect('account')

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
            messages.success('Project updated successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile: Profile = request.user.profile
    project: Project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        messages.success('Project deleted successfully!')
        return redirect('account')
    context = {'object': project}
    return render(request, 'delete_template.html', context)
