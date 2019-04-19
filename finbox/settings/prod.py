from .base      import *
from subprocess import check_output

DEBUG         = False
SECRET_KEY    = '1eeb96e4-d97b-4610-b383-9b1bcd7a2edf'
ALLOWED_HOSTS = ['finbox.themrinalsinha.com']
GIT_COMMIT_ID = check_output("git describe --tags --always --long", shell=True).strip()
