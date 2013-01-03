from django.core.management import setup_environ
import settings

setup_environ(settings)

from prizes.dbcopy import *
check_and_copy()
