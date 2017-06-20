import sys, os

import urllib.parse as urlparse
from urllib.parse import urlencode
from django.template import loader


def is_sphinx_autodoc_running():
    """
    Utility to work out whether the sphinx autodoc module is currently running.

    This can be handy to know since autodoc will attempt to import modules that
    may otherwise assume they are running in a django web app environment.

    Returns True or False
    """
    calling_command = os.path.split(sys.argv[0])[-1]
    return calling_command == 'sphinx-build'

def add_params_to_url(url, **params):
    """
    Reliably add a dictionary of GET parameters to a url string.

    Args:
      - `url` - string - the URL string
      - `**params` - kwargs - the GET key/value parameter pairs to add to the URL

    Returns:
      The updated URL string.
    """
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)

def add_path_to_url(url, path):
    """
    Reliably add a path to the end of a url.

    Args:
      - `url` - string - the URL string
      - `path` - string - the path to append to the url

    Returns:
      The updated URL string.
    """
    if url.endswith('/'):
        url = url[:-1]
    if not path.startswith('/'):
        path = '/' + path
    return url + path

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

def get_form_error_dict(form):
    """
    Given a django form, collect the errors in to a string: string mapping.
    A normal form error dictionary will have a list of errors for each value.

    Args:
      * `form` - Form - the form with errors

    Returns:
      A string:string dictionary with keys as form fields and values as a comma
      delimited string of error messages.
    """
    errors = {f_name: ', '.join([val for val in values]) 
        for f_name, values in form.errors.items()}
    return errors
