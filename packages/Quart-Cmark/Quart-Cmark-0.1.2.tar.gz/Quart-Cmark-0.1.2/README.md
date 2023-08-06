# quart-cmark

Add [CommonMark](https://commonmark.org/) processing [filter](http://jinja.pocoo.org/docs/2.10/templates/#filters) to your `Quart` app, using [paka.cmark](https://github.com/kapyshin/paka.cmark) because why should I do any work?

`paka.cmark` uses the [commonmark/cmark](https://github.com/commonmark/cmark) reference implementation, so it should render anything outlined in the [CommonMark Spec](https://spec.commonmark.org/) lickety-split. 

Source code may be found at [Gitlab](https://gitlab.com/doug.shawhan/quart-cmark).

Docs at [readthedocs](https://quart-cmark.readthedocs.io).

# Installation

```bash
pip install Quart-Cmark
```

# Usage

## Script

```python
from quart_cmark import Cmark
cm = Cmark(app)
```

or, if you are using factory pattern:

```python
from quart_cmark import Cmark
cm = Cmark()
cm.init_app(app)
```

Create routes in the usual way:
```python
@app.route("/markdown-fest")
async def markdown_fest():
    mycm = u"Hello, *commonmark* block."
    return await render_template("markdown-fest.html", mycm=mycm) 
```

## Template

### Inline-style

```html
<html>
{{mycm|commonmark}}
</html>
```

### Block-style

```html
<html>
{% filter commonmark %}
{{mycm}}
{% endfilter %}
</html>
```

## Autoescape

Jinja2's autoescape works when declared at init. See [tests](https://gitlab.com/doug.shawhan/quart-cmark/blob/master/tests/test_cmark.py) for examples.

## Tests

`pytest`
