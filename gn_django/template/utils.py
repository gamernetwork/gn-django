import os

from django.template import loader
from jinja2.environment import Environment

def render_to_string(template, context, request=None, using=None):
    """
    Shortcut for rendering templates using the current django project's collection
    of loaders.
    
    Args:
      * `template` - string - the template to render
      * `context` - mapping - the template context
    Kwargs:
      * `request` - HttpRequest - the current request, if available
      * `using` - 

    Returns:
      The rendered template string.
    """
    return loader.render_to_string(template, context=context, request=request, using=using)

def render_from_string(template_string, context):
    """
    Shortcut for using simple strings as templates, e.g. '<p>{{ foo }}</p>'

    Args:
      * `template_string` - string - the string to use as a template
      * `context` - mapping - the template context

    Return:
      The rendered template string
    """
    return Environment().from_string(template_string).render(context)

def get_template_dir_for_app(app_name):
    """
    Get the absolute path to an app's template directory, given the app name.

    Args:
      * `app_name` - string - the name of the django app

    Returns:
      The absolute path to the template directory.
    """
    app_module = __import__(app_name, fromlist=[''])
    app_path = os.path.dirname(app_module.__file__)
    template_path = os.path.join(app_path, 'templates')
    return template_path