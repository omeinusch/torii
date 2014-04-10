from django.shortcuts import render, get_object_or_404
from models import News

from roadmap.models import Release, Milestone, Commit


def homepage(request):
    try:
        latest_release = Release.objects.filter(stable=True).latest()
    except Release.DoesNotExist:
        try:
            latest_release = Release.objects.latest()
        except Release.DoesNotExist:
            latest_release = None

    try:
        announcement = News.objects.latest()
    except News.DoesNotExist:
        announcement = None

    try:
        latest_commit = Commit.objects.latest()
    except Commit.DoesNotExist:
        latest_commit = None

    c = {
        'latest_release': latest_release,
        'announcement': announcement,
        'latest_commit': latest_commit,
    }

    return render(request, 'content/homepage.html', c)


def news(request):
    news_list = News.objects.all()
    return render(request, 'content/news.html', {'news_list': news_list})


def releases(request):
    milestones = Milestone.objects.all()
    return render(request, 'roadmap/index.html', {'milestones': milestones})


def releases_detail(request, milestone_title):
    milestone = get_object_or_404(Milestone, title=milestone_title)
    return render(request, 'roadmap/detail.html', {'milestone': milestone})


def downloads(request):
    try:
        latest_unstable = Release.objects.filter(stable=False).latest()
    except Release.DoesNotExist:
        latest_unstable = None

    try:
        latest_stable = Release.objects.filter(stable=True).latest()
    except Release.DoesNotExist:
        latest_stable = None

    try:
        latest_commit = Commit.objects.latest()
    except Commit.DoesNotExist:
        latest_commit = None


    c = {
        'latest_unstable': latest_unstable,
        'latest_stable': latest_stable,
        'latest_commit': latest_commit,
    }
    return render(request, 'content/downloads.html', c)


def support(request):
    return render(request, 'content/support.html')


def news_detail(request, news_slug):
    single_news = get_object_or_404(News, slug=news_slug)
    return render(request, 'content/news-detail.html', {'news': single_news})
