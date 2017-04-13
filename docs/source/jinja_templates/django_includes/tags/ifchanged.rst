.. templatetag:: ifchanged

``ifchanged``
-------------

Check if a value has changed from the last iteration of a loop.

The ``{% ifchanged %}`` block tag is used within a loop. It has two possible
uses.

1. Checks its own rendered contents against its previous state and only
   displays the content if it has changed. For example, this displays a list of
   days, only displaying the month if it changes::

        <h1>Archive for {{ year }}</h1>

        {% for date in days %}
            {% ifchanged %}<h3>{{ date|date:"F" }}</h3>{% endifchanged %}
            <a href="{{ date|date:"M/d"|lower }}/">{{ date|date:"j" }}</a>
        {% endfor %}

2. If given one or more variables, check whether any variable has changed.
   For example, the following shows the date every time it changes, while
   showing the hour if either the hour or the date has changed::

        {% for date in days %}
            {% ifchanged date.date %} {{ date.date }} {% endifchanged %}
            {% ifchanged date.hour date.date %}
                {{ date.hour }}
            {% endifchanged %}
        {% endfor %}

The ``ifchanged`` tag can also take an optional ``{% else %}`` clause that
will be displayed if the value has not changed::

        {% for match in matches %}
            <div style="background-color:
                {% ifchanged match.ballot_id %}
                    {% cycle "red" "blue" %}
                {% else %}
                    gray
                {% endifchanged %}
            ">{{ match }}</div>
        {% endfor %}

