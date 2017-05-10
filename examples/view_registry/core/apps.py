from gn_django.app import GNAppConfig

from . import views

class CoreConfig(GNAppConfig):
    name = 'core'
    views = {
        'core:Home': views.Home,
    }
