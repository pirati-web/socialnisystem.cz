from django.conf import settings


def global_info(request):
    return {
        'siteinfo': settings.SITEINFO,
        'footer_menu': settings.FOOTER_MENU,
    }
