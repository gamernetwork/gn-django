.. templatetag:: widthratio

.. function:: widthratio

    For creating bar charts and such, this tag calculates the ratio of a given
    value to a maximum value, and then applies that ratio to a constant.
    
    For example::
    
        <img src="bar.png" alt="Bar"
             height="10" width="{% widthratio this_value max_value max_width %}" />
    
    If ``this_value`` is 175, ``max_value`` is 200, and ``max_width`` is 100, the
    image in the above example will be 88 pixels wide
    (because 175/200 = .875; .875 * 100 = 87.5 which is rounded up to 88).
    
    In some cases you might want to capture the result of ``widthratio`` in a
    variable. It can be useful, for instance, in a :ttag:`blocktrans` like this::
    
        {% widthratio this_value max_value max_width as width %}
        {% blocktrans %}The width is: {{ width }}{% endblocktrans %}
    