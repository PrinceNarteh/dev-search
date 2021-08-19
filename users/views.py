from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .models import Profile, Skill
from projects.models import Project


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username not found.')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect.')
    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info("User successfully logout.")
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created!")
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, "Error occurred durring registration!")
    context = {"page": page, "form": form}

    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'users/profiles.html', {"profiles": profiles})


def userProfile(request, pk: str):
    profile: Profile = Profile.objects.get(id=pk)
    top_skills: list[Skill] = profile.skill_set.exclude(description__exact="")
    other_skills: list[Skill] = profile.skill_set.filter(description="")
    context = {"profile": profile, "top_skills": top_skills,
               "other_skills": other_skills}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile: Profile = request.user.profile
    skills: list[Skill] = profile.skill_set.all()
    projects: list[Project] = profile.project_set.all()
    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile: Profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {"form": form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url="login")
def createSkill(request):
    profile: Profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill: Skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    context = {"form": form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url="login")
def updateSkill(request, pk):
    profile: Profile = request.user.profile
    skill: Skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {"form": form}
    return render(request, 'users/skill_form.html', context)
