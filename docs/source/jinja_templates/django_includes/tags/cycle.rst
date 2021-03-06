.. templatetag:: cycle

.. function:: cycle

    Produces one of its arguments each time this tag is encountered. The first
    argument is produced on the first encounter, the second argument on the second
    encounter, and so forth. Once all arguments are exhausted, the tag cycles to
    the first argument and produces it again.
    
    This tag is particularly useful in a loop::
    
        {% for o in some_list %}
            <tr class="{% cycle 'row1' 'row2' %}">
                ...
            </tr>
        {% endfor %}
    
    The first iteration produces HTML that refers to class ``row1``, the second to
    ``row2``, the third to ``row1`` again, and so on for each iteration of the
    loop.
    
    You can use variables, too. For example, if you have two template variables,
    ``rowvalue1`` and ``rowvalue2``, you can alternate between their values like
    this::
    
        {% for o in some_list %}
            <tr class="{% cycle rowvalue1 rowvalue2 %}">
                ...
            </tr>
        {% endfor %}
    
    Variables included in the cycle will be escaped.  You can disable auto-escaping
    with::
    
        {% for o in some_list %}
            <tr class="{% autoescape off %}{% cycle rowvalue1 rowvalue2 %}{% endautoescape %}">
                ...
            </tr>
        {% endfor %}
    
    You can mix variables and strings::
    
        {% for o in some_list %}
            <tr class="{% cycle 'row1' rowvalue2 'row3' %}">
                ...
            </tr>
        {% endfor %}
    
    In some cases you might want to refer to the current value of a cycle
    without advancing to the next value. To do this,
    just give the ``{% cycle %}`` tag a name, using "as", like this::
    
        {% cycle 'row1' 'row2' as rowcolors %}
    
    From then on, you can insert the current value of the cycle wherever you'd like
    in your template by referencing the cycle name as a context variable. If you
    want to move the cycle to the next value independently of the original
    ``cycle`` tag, you can use another ``cycle`` tag and specify the name of the
    variable. So, the following template::
    
        <tr>
            <td class="{% cycle 'row1' 'row2' as rowcolors %}">...</td>
            <td class="{{ rowcolors }}">...</td>
        </tr>
        <tr>
            <td class="{% cycle rowcolors %}">...</td>
            <td class="{{ rowcolors }}">...</td>
        </tr>
    
    would output::
    
        <tr>
            <td class="row1">...</td>
            <td class="row1">...</td>
        </tr>
        <tr>
            <td class="row2">...</td>
            <td class="row2">...</td>
        </tr>
    
    You can use any number of values in a ``cycle`` tag, separated by spaces.
    Values enclosed in single quotes (``'``) or double quotes (``"``) are treated
    as string literals, while values without quotes are treated as template
    variables.
    
    By default, when you use the ``as`` keyword with the cycle tag, the
    usage of ``{% cycle %}`` that initiates the cycle will itself produce
    the first value in the cycle. This could be a problem if you want to
    use the value in a nested loop or an included template. If you only want
    to declare the cycle but not produce the first value, you can add a
    ``silent`` keyword as the last keyword in the tag. For example::
    
        {% for obj in some_list %}
            {% cycle 'row1' 'row2' as rowcolors silent %}
            <tr class="{{ rowcolors }}">{% include "subtemplate.html" %}</tr>
        {% endfor %}
    
    This will output a list of ``<tr>`` elements with ``class``
    alternating between ``row1`` and ``row2``. The subtemplate will have
    access to ``rowcolors`` in its context and the value will match the class
    of the ``<tr>`` that encloses it. If the ``silent`` keyword were to be
    omitted, ``row1`` and ``row2`` would be emitted as normal text, outside the
    ``<tr>`` element.
    
    When the silent keyword is used on a cycle definition, the silence
    automatically applies to all subsequent uses of that specific cycle tag.
    The following template would output *nothing*, even though the second
    call to ``{% cycle %}`` doesn't specify ``silent``::
    
        {% cycle 'row1' 'row2' as rowcolors silent %}
        {% cycle rowcolors %}
    
    You can use the :ttag:`resetcycle` tag to make a ``{% cycle %}`` tag restart
    from its first value when it's next encountered.
    