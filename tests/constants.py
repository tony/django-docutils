"""Constants for Django Docutils test suite."""

DEFAULT_RST = r"""
hey
---

hi
##

A. hows
B. it

C. going
D. today

**hi**
*hi*
"""

DEFAULT_RST_WITH_SECTIONS = """
hey
---

hi
##

My first section
----------------

Some text

My second section
-----------------

Additional text

A. hows
B. it

C. going
D. today

**hi**
*hi*
"""


DEFAULT_EXPECTED_CONTENT = r"""
<ol class="upperalpha simple">
<li><p>hows</p></li>
<li><p>it</p></li>
<li><p>going</p></li>
<li><p>today</p></li>
</ol>
<p><strong>hi</strong>
<em>hi</em></p>
""".strip()
DEFAULT_EXPECTED = rf"""
<main id="hey">
<h1 class="title is-1">hey</h1>
<p class="subtitle" id="hi">hi</p>
{DEFAULT_EXPECTED_CONTENT}
</main>

"""
