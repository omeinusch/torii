from content.models import Configuration, Phrases


def context(request):
    return {
        'path': request.path.split('/')[1],
        'configuration': Configuration.objects.first(),
        'phrases': Phrases(),
    }
