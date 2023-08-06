"""
quart_cmark
----------------

Cmark filter class for Quart. I did the bare minimum i.e: decorating
``paka.cmark`` with ``template_filter`` to make the call useful for Quart.

- https://pgjones.gitlab.io/quart/reference/source/quart.app.html#quart.app.Quart.template_filter
- https://pgjones.gitlab.io/quart/how_to_guides/templating.html#adding-filters-tests-globals-and-context

Uses ``paka.cmark`` since I'm too lazy to do the hard work with ctypes.

See https://commonmark.org/ for details on how commonmark works.

See https://github.com/commonmark/cmark for info on the CommonMark reference
library that ``paka.cmark`` uses.

Usage
::
    from quart_cmark import Cmark
    cm = Cmark(app)

    # or, if you are using the factory pattern

    cm = Cmark()
    cm.init_app(app)

    # Create routes in the usual way
    @app.route("/commonmark")
    def display_commonmark():
        mycm = u"Hello, *commonmark* block."
        return render_template("commonmark.html", mycm=mycm)


Templates
::
    # one can just place raw markdown in the template. The filter expects
    # your markdown to be fully left-aligned! Otherwise expect plaintext.
    {% filter commonmark %}
    # Nagasaki
    1. Chew Terbaccy
    1. Wicky-waky-woo
    {% endfilter %}

    # block style
    {% filter commonmark %}{{ mycm }}{% endfilter %}

    # inline style
    {{mycm|commonmark}}

:copyright: (c) 2022 by Doug Shawhan.
:license: BSD, MIT see LICENSE for details.
"""

from typing import Union, Literal

import quart
from quart import Markup
import markupsafe

from paka import cmark


class Cmark:
    """
    Cmark
    -----

    Wrapper class for Cmark (aka "common markdown"), objects.

    Args:
        app (obj):  Quart app instance
        auto_escape (bool): Use Jinja2 auto_escape, default False
    """

    def __init__(
        self, app: Union[bool, quart.app.Quart] = False, auto_escape: bool = False
    ):
        """
        Create parser and renderer objects and auto_escape value.
        Set filter.

        Args:
            app (Union[bool, quart.app.Quart]): quart app object
            auto_escape (bool): Shall we auto escape?
        """

        if not app:
            return

        self.init_app(app, auto_escape)


    def init_app(self, app: quart.app.Quart, auto_escape: bool = False) -> None:
        """
        Initialze the commonmark filter.
        """

        @app.template_filter(name="commonmark")
        def commonmark_filter(markdown_text: str) -> markupsafe.Markup:
            """
            Sorry, escape cannot be set in templates.

            Args:
                markdown_text (str): markdown to translate to html
            Returns:
                html (str): html from markdown
            """

            html = cmark.to_html(markdown_text, safe=False)

            if auto_escape:
                return Markup(markupsafe.escape(html))

            return Markup(html)

        self.commonmark_filter = commonmark_filter


    def __call__(self, stream: markupsafe.Markup) -> str:
        """
        Render markdown stream.

        Args:
            stream (str): template stream containing markdown tags

        Returns:
            html (str): markdown rendered as html
        """

        return self.commonmark_filter(stream)
