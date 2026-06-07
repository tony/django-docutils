(faq)=

# FAQ

## General

New to the ecosystem? {ref}`what-is-docutils` maps docutils,
reStructuredText, Sphinx, and Markdown in one page.

### What is reST, RST, reStructuredText?

[reStructuredText] is a markup syntax, similar to markdown. Learn it from the
official [primer][rst-primer] and [quick reference][rst-quickref].

[rst-primer]: https://docutils.sourceforge.io/docs/user/rst/quickstart.html
[rst-quickref]: https://docutils.sourceforge.io/docs/user/rst/quickref.html

### What is docutils?

[docutils] is a python package for parsing and publishing markup. The default docutils package
supports reStructuredText. It can also parse markdown when a third-party
parser such as [myst-docutils] or [myst-parser] is installed — see
{ref}`what-is-docutils` for the details.

[myst-docutils]: https://pypi.org/project/myst-docutils/
[myst-parser]: https://myst-parser.readthedocs.io/

## Django Docutils

### Do I need this package to parse reStructuredText in Django?

No! [docutils] can always be used directly.

This package simply offers template extensions to use docutils in django views.

### What does this package provide?

3 ways to render reStructuredText via docutils in [Django]:

1. {ref}`template_tag`
2. {ref}`template_filter`
3. {ref}`class_based_view`

### Can I copy code from this project to my own?

Yes! Go ahead, the project's source is released under the [MIT license] - you are welcome to view the codebase and copy just
what you need.

[MIT license]: https://github.com/tony/django-docutils/blob/master/LICENSE
[docutils]: https://docutils.sourceforge.io/
[reStructuredText]: https://docutils.sourceforge.io/rst.html
[Django]: https://docs.djangoproject.com/
