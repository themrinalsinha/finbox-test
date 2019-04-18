from django.conf import settings

def context(request):
    return {
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'GIT_COMMIT_ID': settings.GIT_COMMIT_ID,
        'PROJECT_REPO' : settings.PROJECT_REPO,
    }
