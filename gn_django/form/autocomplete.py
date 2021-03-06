from dal_select2.views import Select2QuerySetView
from django.db import models
from django import forms
from dal import autocomplete

class SelectWidget(autocomplete.Select2):
    """
    Widget for autocomplete select fields to be added to forms. Is almost identical
    to Django Autocomplete Light's Select2 widget, but fixes the issue where the
    selected value will not display if the options are not loaded from a Django query set.

    Since the widget has no direct way of knowing the label for the selected value, by
    default it will be the same as the value. However, the ``label_finder`` parameter
    allows developers to pass a callable to the class to determine the label. The
    callable must take only the selected value as a parameter.
    """
    def __init__(self, label_finder=None, *args, **kwargs):
        if label_finder:
            self.get_label = label_finder
        super().__init__(*args, **kwargs)

    def filter_choices_to_render(self, selected_choices):
        """
        Pre-populate form if value is set. The value should be the only item in
        the ``selected_choices`` list. If the callable ``label_finder`` parameter was set on
        initialization (or ``get_label`` attribute has been declared elsewhere),
        the value will be run through that to get the label for the option with
        that value.
        """
        if selected_choices:
            selected = selected_choices[0]
            if hasattr(self, 'get_label') and selected_choices:
                label = self.get_label(selected)
                if label:
                    self.choices = ((selected, label),)
            else:
                self.choices = ((selected, selected),)

class AutocompleteView(Select2QuerySetView):
    """
    Base view for populating autocomplete form fields. When the user starts typing
    the form field, the field will be populated with suggestions based on the
    `get_option_list()` method, which will need to be declared.
    """
    def get_option_list(self):
        """
        Get values to populate suggestions on autocomplete form field. The value
        entered into the autocomplete box is set to ``self.q``

        Suggestions can be returned in the following formats:

        - An iterable of suggestions - These suggestions will appear as both the label
            and value of the form field
        - An iterable of dictionaries - The dictionary should have a ``label`` key
            and a ``value`` key. If the ``value`` is not set, it will default to the ``label``.
            If the ``label`` is not set, it will error. The ``label`` will be displayed
            in the suggestion list, and the ``value`` will be submitted.

        Note: If returning a list, it would be wise to sort it first as otherwise
        the order of suggestions may be inconsistent
        """
        raise NotImplementedError('Must declare `get_option_list()` method on class that extends `gn_django.form.autocomplete.AutocompleteView`')

    def get_result_value(self, result):
        """
        Get the value from the list returned by ``get_option_list()``. If the
        current iteration is dictionary, it will check for the ``value``, and
        if that does not exist, will take the value of the ``label`` key. Otherwise
        it will take the value as is.

        Returns:
            - If the resulting value is an instance of ``django.db.models.Model``,
            it will return the ``pk`` attribute. Otherwise, it will return the value
            as is.
        """
        if isinstance(result, dict):
            result = result.get('value', result['label'])
        if isinstance(result, models.Model):
            result = result.pk
        return result

    def get_result_label(self, result):
        """
        Get the label from the list returned by ``get_option_list()``. If the
        current iteration is a dictionary, it will return the value assigned to
        the ``label`` key. Otherwise, it will return the value as is.
        """
        if isinstance(result, dict):
            return result['label']
        return result

    def get_context_data(self, *args, **kwargs):
        """
        Override `get_context_data()` to reset `object_list` to value declared in `get_option_list()`
        """
        return super(AutocompleteView, self).get_context_data(object_list=self.get_option_list(), *args, **kwargs)

    def get_queryset(self):
        """
        Bypass `get_queryset()`. The `django-autocomplete-light` extension assumes
        that the autocomplete field will be used in conjunction with the Django ORM.
        Instead, logic to load autocomplete suggestions should be in `get_option_list()`
        """
        return
