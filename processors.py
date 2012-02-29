from django.conf import settings

def chamanesconf(request):
    dictionary = {
        'site_url': settings.SITE_URL,
        'site_name': settings.SITE_NAME,
    }

    return dictionary

