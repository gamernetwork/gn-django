from jinja2 import nodes, exceptions, runtime, environment
from jinja2.ext import Extension
from django.conf import settings as dj_settings
from django.core import exceptions

import re

class SpacelessExtension(Extension):
    """
    Removes whitespace between HTML tags at compile time, including tab and newline characters.
    It does not remove whitespace between jinja2 tags or variables. Neither does it remove whitespace between tags
    and their text content.
    Adapted from coffin:
        https://github.com/coffin/coffin/blob/master/coffin/template/defaulttags.py
    Usage:
        ``{% spaceless %}fooo bar baz{% endspaceless %}``
    """

    tags = set(['spaceless'])

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(['name:endspaceless'], drop_needle=True)
        return nodes.CallBlock(
            self.call_method('_strip_spaces', [], [], None, None),
            [], [], body,
        ).set_lineno(lineno)

    def _strip_spaces(self, caller=None):
        return re.sub(r'>\s+<', '><', caller().strip())

class IncludeWithExtension(Extension):
    """
    Includes a template with an explicitly declared context.
    Usage:
        ``{% include_with 'sometemplate.j2' foo='bar', hello=['world'] %}``
    """

    tags = set(['include_with'])

    def parse(self, parser):
        # First part will be 'include_with' tag, but also contains line number which
        # we use
        first = parser.parse_expression()

        # Second part is the template name
        template = parser.parse_expression()

        # Grab the context variables
        context = self._get_params(parser)
        call = self.call_method('_render', [template, context], lineno=first.lineno)

        return nodes.CallBlock(call, [], [], [], lineno=first.lineno)

    def _render(self, template, context, caller):
        """
        Render the template with context variables

        Params:
            - `template` - The name of the template to render
            - `context` - The context to pass to the template
            - `caller` - Required by Jinja2

        Returns:
            - The parsed template
        """
        return self.environment.get_template(template).render(context)

    def _get_params(self, parser):
        """
        Parses the statement to collect the parameters given

        Returns:
            - `nodes.Dict` - A dictionary node containing instances of `nodes.Pair` representing
                the key/value pairs in the context
        """
        # Argument parsing adapted from https://github.com/coffin/coffin/blob/master/coffin/common.py#L164
        stream = parser.stream
        kwargs = []
        eval_ctx = nodes.EvalContext(self.environment)
        while not stream.current.test_any('block_end'):
            if kwargs:
                stream.expect('comma')
            if stream.current.test('name') and stream.look().test('assign'):
                key = nodes.Const(next(stream).value)
                stream.skip()
                value = parser.parse_expression()
                kwargs.append(nodes.Pair(key, value, lineno=key.lineno))
        if not kwargs:
            parser.fail('`include_with` tag must have parameters. Use `include` instead', lineno=stream.current.lineno)

        kwargs = nodes.Dict(kwargs)

        return kwargs

class CSSExtension(Extension):
    tags = set(['css', 'compile_less'])

    def __init__(self, *args, **kwargs):
        self.debug_less = self._debug_less()

        return super(CSSExtension, self).__init__(*args, **kwargs)

    def parse(self, parser):
        first = parser.parse_expression()
        if first.name == 'css':
            name = parser.parse_expression()
            call = self.call_method('_css', [name], lineno=first.lineno)
        elif first.name == 'compile_less':
            call = self.call_method('_compile_less', lineno=first.lineno)

        return nodes.CallBlock(call, [], [], [], lineno=first.lineno)

    def _css(self, name, caller):
        ext = 'css'
        if self.debug_less:
            ext = 'less'
        file_dir = self._get_file_dir(ext)

        template = '<link href="{{ static("%s/%s.%s") }}?v={{ randint(minimum=0,maximum=99999) }}" rel="stylesheet" type="text/%s" />' % (file_dir, name, ext, ext)

        return self.environment.from_string(template).render()

    def _compile_less(self, caller):
        if not self.debug_less:
            return self.environment.from_string('').render()

        if not hasattr(dj_settings, 'CLIENT_LESS_COMPILER'):
            raise exceptions.ImproperlyConfigured('Cannot compile LESS on frontend, `CLIENT_LESS_COMPILER` must be configured.')
        template = """
<script src="%s"></script>
<script>
    localStorage.clear();
    less = { env: "development" }
</script>
""" % dj_settings.CLIENT_LESS_COMPILER

        return self.environment.from_string(template).render()

    def _debug_less(self):
        if hasattr(dj_settings, 'DEBUG_LESS'):
            return dj_settings.DEBUG_LESS
        return dj_settings.DEBUG

    def _get_file_dir(self, ext):
        if hasattr(dj_settings, 'STATIC_FILE_MAP'):
            return dj_settings.STATIC_FILE_MAP.get(ext, ext)

        return ext
