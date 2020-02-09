import re

from docutils import nodes, utils
from docutils.transforms import Transform

from django_docutils.lib.settings import BASED_LIB_RST

url_patterns = BASED_LIB_RST.get('font_awesome', {}).get('url_patterns', {})


class InjectFontAwesome(Transform):

    default_priority = 680

    def apply(self):
        for target in self.document.traverse(nodes.reference):
            if target.hasattr('refuri'):
                url = target['refuri']
                for url_pattern, classes in url_patterns.items():
                    if re.match(url_pattern, url):

                        fa_tag = f'<em class="{classes}"></em>'
                        title = utils.unescape(target[0])
                        rn = nodes.reference('', '', internal=True, refuri=url)
                        rn += nodes.raw('', fa_tag, format='html')
                        rn += nodes.Text(title, title)
                        target.replace_self(rn)
                        break
