.. templatefilter:: add

.. function:: add

    Adds the argument to the value.
    
    For example::
    
        {{ value|add("2") }}
    
    If ``value`` is ``4``, then the output will be ``6``.
    
    This filter will first try to coerce both values to integers. If this fails,
    it'll attempt to add the values together anyway. This will work on some data
    types (strings, list, etc.) and fail on others. If it fails, the result will
    be an empty string.
    
    For example, if we have::
    
        {{ first|add(second) }}
    
    and ``first`` is ``[1, 2, 3]`` and ``second`` is ``[4, 5, 6]``, then the
    output will be ``[1, 2, 3, 4, 5, 6]``.
    
    .. warning::
    
        Strings that can be coerced to integers will be **summed**, not
        concatenated, as in the first example above.
    