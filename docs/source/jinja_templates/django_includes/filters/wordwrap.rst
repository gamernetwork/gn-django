.. templatefilter:: wordwrap

.. function:: wordwrap

    Wraps words at specified line length.
    
    **Argument:** number of characters at which to wrap the text
    
    For example::
    
        {{ value|wordwrap:5 }}
    
    If ``value`` is ``Joel is a slug``, the output would be::
    
        Joel
        is a
        slug
    