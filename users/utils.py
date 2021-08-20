from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.query_utils import Q
from users.models import Profile, Skill

def paginate_profiles(request, profiles, results_per_page):

    page = request.GET.get('page')
    paginator = Paginator(profiles, results_per_page)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(1)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles


def search_profiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills: list[Skill] = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    )

    return profiles, search_query
