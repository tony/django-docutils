(faq)=

# FAQ

## General

### What is reST, RST, reStructuredText?

[reStructuredText] is a markup syntax, similar to markdown.

### What is docutils?

[docutils] is a python package for parsing and publishing markup. The default docutils package
supports reStructuredText. It can also be extended to parse markdown
(e.g. [myst-parser]).

[myst-parser]: https://github.com/executablebooks/MyST-Parser

## Django Docutils

### Do I need this package to parse reStructuredText in Django?

No! [docutils] can always be used directly.

This package simply offers template extensions to use docutils in django views.

### What does this package provide?

3 ways to render reStructuredText via docutils in [Django]:

1. {ref}`class_based_view`
2. {ref}`template_tag`
3. {ref}`template_filter`

### Can I copy code from this project to my own?

Yes! Go ahead, the project's source is released under the [MIT license] - you are welcome to view the codebase and copy just
what you need.

[MIT license]: https://github.com/tony/django-docutils/blob/master/LICENSE
[docutils]: https://docutils.sourceforge.io/
[reStructuredText]: https://docutils.sourceforge.io/rst.html
[Django]: https://docs.djangoproject.com/
