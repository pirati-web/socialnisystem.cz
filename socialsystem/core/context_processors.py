from django.conf import settings


def siteinfo(request):
    return {
        'siteinfo': settings.SITEINFO
    }
