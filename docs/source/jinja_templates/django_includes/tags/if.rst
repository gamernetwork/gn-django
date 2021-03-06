.. templatetag:: if

.. function:: if

    The ``{% if %}`` tag evaluates a variable, and if that variable is "true" (i.e.
    exists, is not empty, and is not a false boolean value) the contents of the
    block are output::
    
        {% if athlete_list %}
            Number of athletes: {{ athlete_list|length }}
        {% elif athlete_in_locker_room_list %}
            Athletes should be out of the locker room soon!
        {% else %}
            No athletes.
        {% endif %}
    
    In the above, if ``athlete_list`` is not empty, the number of athletes will be
    displayed by the ``{{ athlete_list|length }}`` variable.
    
    As you can see, the ``if`` tag may take one or several ``{% elif %}``
    clauses, as well as an ``{% else %}`` clause that will be displayed if all
    previous conditions fail. These clauses are optional.
    
    Boolean operators
    ~~~~~~~~~~~~~~~~~
    
    :ttag:`if` tags may use ``and``, ``or`` or ``not`` to test a number of
    variables or to negate a given variable::
    
        {% if athlete_list and coach_list %}
            Both athletes and coaches are available.
        {% endif %}
    
        {% if not athlete_list %}
            There are no athletes.
        {% endif %}
    
        {% if athlete_list or coach_list %}
            There are some athletes or some coaches.
        {% endif %}
    
        {% if not athlete_list or coach_list %}
            There are no athletes or there are some coaches.
        {% endif %}
    
        {% if athlete_list and not coach_list %}
            There are some athletes and absolutely no coaches.
        {% endif %}
    
    Use of both ``and`` and ``or`` clauses within the same tag is allowed, with
    ``and`` having higher precedence than ``or`` e.g.::
    
        {% if athlete_list and coach_list or cheerleader_list %}
    
    will be interpreted like:
    
    .. code-block:: python
    
        if (athlete_list and coach_list) or cheerleader_list
    
    Use of actual parentheses in the :ttag:`if` tag is invalid syntax. If you need
    them to indicate precedence, you should use nested :ttag:`if` tags.
    
    :ttag:`if` tags may also use the operators ``==``, ``!=``, ``<``, ``>``,
    ``<=``, ``>=``, ``in``, ``not in``, ``is``, and ``is not`` which work as
    follows:
    
    ``==`` operator
    ^^^^^^^^^^^^^^^
    
    Equality. Example::
    
        {% if somevar == "x" %}
          This appears if variable somevar equals the string "x"
        {% endif %}
    
    ``!=`` operator
    ^^^^^^^^^^^^^^^
    
    Inequality. Example::
    
        {% if somevar != "x" %}
          This appears if variable somevar does not equal the string "x",
          or if somevar is not found in the context
        {% endif %}
    
    ``<`` operator
    ^^^^^^^^^^^^^^
    
    Less than. Example::
    
        {% if somevar < 100 %}
          This appears if variable somevar is less than 100.
        {% endif %}
    
    ``>`` operator
    ^^^^^^^^^^^^^^
    
    Greater than. Example::
    
        {% if somevar > 0 %}
          This appears if variable somevar is greater than 0.
        {% endif %}
    
    ``<=`` operator
    ^^^^^^^^^^^^^^^
    
    Less than or equal to. Example::
    
        {% if somevar <= 100 %}
          This appears if variable somevar is less than 100 or equal to 100.
        {% endif %}
    
    ``>=`` operator
    ^^^^^^^^^^^^^^^
    
    Greater than or equal to. Example::
    
        {% if somevar >= 1 %}
          This appears if variable somevar is greater than 1 or equal to 1.
        {% endif %}
    
    ``in`` operator
    ^^^^^^^^^^^^^^^
    
    Contained within. This operator is supported by many Python containers to test
    whether the given value is in the container. The following are some examples
    of how ``x in y`` will be interpreted::
    
        {% if "bc" in "abcdef" %}
          This appears since "bc" is a substring of "abcdef"
        {% endif %}
    
        {% if "hello" in greetings %}
          If greetings is a list or set, one element of which is the string
          "hello", this will appear.
        {% endif %}
    
        {% if user in users %}
          If users is a QuerySet, this will appear if user is an
          instance that belongs to the QuerySet.
        {% endif %}
    
    ``not in`` operator
    ^^^^^^^^^^^^^^^^^^^
    
    Not contained within. This is the negation of the ``in`` operator.
    
    ``is`` operator
    ^^^^^^^^^^^^^^^
    
    Object identity. Tests if two values are the same object. Example::
    
        {% if somevar is True %}
          This appears if and only if somevar is True.
        {% endif %}
    
        {% if somevar is None %}
          This appears if somevar is None, or if somevar is not found in the context.
        {% endif %}
    
    ``is not`` operator
    ^^^^^^^^^^^^^^^^^^^
    
    Negated object identity. Tests if two values are not the same object. This is
    the negation of the ``is`` operator. Example::
    
        {% if somevar is not True %}
          This appears if somevar is not True, or if somevar is not found in the
          context.
        {% endif %}
    
        {% if somevar is not None %}
          This appears if and only if somevar is not None.
        {% endif %}
    
    Filters
    ~~~~~~~
    
    You can also use filters in the :ttag:`if` expression. For example::
    
        {% if messages|length >= 100 %}
           You have lots of messages today!
        {% endif %}
    
    Complex expressions
    ~~~~~~~~~~~~~~~~~~~
    
    All of the above can be combined to form complex expressions. For such
    expressions, it can be important to know how the operators are grouped when the
    expression is evaluated - that is, the precedence rules. The precedence of the
    operators, from lowest to highest, is as follows:
    
    * ``or``
    * ``and``
    * ``not``
    * ``in``
    * ``==``, ``!=``, ``<``, ``>``, ``<=``, ``>=``
    
    (This follows Python exactly). So, for example, the following complex
    :ttag:`if` tag::
    
        {% if a == b or c == d and e %}
    
    ...will be interpreted as:
    
    .. code-block:: python
    
        (a == b) or ((c == d) and e)
    
    If you need different precedence, you will need to use nested :ttag:`if` tags.
    Sometimes that is better for clarity anyway, for the sake of those who do not
    know the precedence rules.
    
    The comparison operators cannot be 'chained' like in Python or in mathematical
    notation. For example, instead of using::
    
        {% if a > b > c %}  (WRONG)
    
    you should use::
    
        {% if a > b and b > c %}
    
    ``ifequal`` and ``ifnotequal``
    ------------------------------
    
    ``{% ifequal a b %} ... {% endifequal %}`` is an obsolete way to write
    ``{% if a == b %} ... {% endif %}``. Likewise, ``{% ifnotequal a b %} ...
    {% endifnotequal %}`` is superseded by ``{% if a != b %} ... {% endif %}``.
    The ``ifequal`` and ``ifnotequal`` tags will be deprecated in a future release.
    