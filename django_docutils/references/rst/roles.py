from docutils import nodes, utils

from django_docutils.lib.utils import split_explicit_title, ws_re

from .nodes import pending_xref
from .utils import set_role_source_info

if False:
    from typing import Type, unicode  # NOQA


class XRefRole:

    """
    A generic cross-referencing role.  To create a callable that can be used as
    a role function, create an instance of this class.

    The general features of this role are:

    * Automatic creation of a reference and a content node.
    * Optional separation of title and target with `title <target>`.
    * The implementation is a class rather than a function to make
      customization easier.

    Customization can be done in two ways:

    * Supplying constructor parameters:
      * `fix_parens` to normalize parentheses (strip from target, and add to
        title if configured)
      * `lowercase` to lowercase the target
      * `nodeclass` and `innernodeclass` select the node classes for
        the reference and the content node

    * Subclassing and overwriting `process_link()` and/or `result_nodes()`.
    """

    nodeclass = pending_xref  # type: Type[nodes.Node]
    innernodeclass = nodes.literal

    def __init__(
        self,
        fix_parens=False,
        lowercase=False,
        nodeclass=None,
        innernodeclass=None,
        warn_dangling=False,
    ):
        # type: (bool, bool, Type[nodes.Node], Type[nodes.Node], bool) -> None
        self.fix_parens = fix_parens
        self.lowercase = lowercase
        self.warn_dangling = warn_dangling
        if nodeclass is not None:
            self.nodeclass = nodeclass
        if innernodeclass is not None:
            self.innernodeclass = innernodeclass

    def _fix_parens(self, env, has_explicit_title, title, target):
        if not has_explicit_title:
            if title.endswith("()"):
                # remove parentheses
                title = title[:-2]
            title += "()"  # add func parens (changed from sphnx, used env)
        # remove parentheses from the target too
        if target.endswith("()"):
            target = target[:-2]
        return title, target

    def __call__(self, typ, rawtext, text, lineno, inliner, options={}, content=[]):
        # env = inliner.document.settings.env
        env = {}
        if not typ:
            typ = env.temp_data.get("default_role")
            if not typ:
                typ = env.config.default_role
            if not typ:
                raise Exception("cannot determine default role!")
        else:
            typ = typ.lower()
        if ":" not in typ:
            domain, role = "", typ  # type: unicode, unicode
            classes = ["xref", role]
        else:
            domain, role = typ.split(":", 1)
            classes = ["xref", domain, f"{domain}-{role}"]
        # if the first character is a bang, don't cross-reference at all
        if text[0:1] == "!":
            text = utils.unescape(text)[1:]
            if self.fix_parens:
                text, tgt = self._fix_parens(env, False, text, "")
            innernode = self.innernodeclass(rawtext, text, classes=classes)
            return self.result_nodes(inliner.document, env, innernode, is_ref=False)
        # split title and target in role content
        has_explicit_title, title, target = split_explicit_title(text)
        title = utils.unescape(title)
        target = utils.unescape(target)
        # fix-up title and target
        if self.lowercase:
            target = target.lower()
        if self.fix_parens:
            title, target = self._fix_parens(env, has_explicit_title, title, target)
        # create the reference node
        refnode = self.nodeclass(
            rawtext, reftype=role, refdomain=domain, refexplicit=has_explicit_title
        )
        # we may need the line number for warnings
        set_role_source_info(inliner, lineno, refnode)  # type: ignore
        title, target = self.process_link(
            env, refnode, has_explicit_title, title, target
        )
        # now that the target and title are finally determined, set them
        refnode["reftarget"] = target
        refnode += self.innernodeclass(rawtext, title, classes=classes)
        # we also need the source document
        refnode["refdoc"] = "docname"  # TODO: pass docname here
        refnode["refwarn"] = self.warn_dangling
        # result_nodes allow further modification of return values
        return self.result_nodes(inliner.document, env, refnode, is_ref=True)

    # methods that can be overwritten

    def process_link(self, env, refnode, has_explicit_title, title, target):
        # type: (BuildEnvironment, nodes.reference, bool, unicode, unicode) -> Tuple[unicode, unicode]  # NOQA
        """Called after parsing title and target text, and creating the
        reference node (given in *refnode*).  This method can alter the
        reference node and must return a new (or the same) ``(title, target)``
        tuple.
        """
        return title, ws_re.sub(" ", target)

    def result_nodes(self, document, env, node, is_ref):
        # type: (nodes.document, BuildEnvironment, nodes.Node, bool) -> Tuple[List[nodes.Node], List[nodes.Node]]  # NOQA
        """Called before returning the finished nodes.  *node* is the reference
        node if one was created (*is_ref* is then true), else the content node.
        This method can add other nodes and must return a ``(nodes, messages)``
        tuple (the usual return value of a role function).
        """
        return [node], []


class PyXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        # type: (BuildEnvironment, nodes.Node, bool, unicode, unicode) -> Tuple[unicode, unicode]  # NOQA
        # refnode['py:module'] = env.ref_context.get('py:module')
        # refnode['py:class'] = env.ref_context.get('py:class')
        if not has_explicit_title:
            title = title.lstrip(".")  # only has a meaning for the target
            target = target.lstrip("~")  # only has a meaning for the title
            # if the first character is a tilde, don't display the module/class
            # parts of the contents
            if title[0:1] == "~":
                title = title[1:]
                dot = title.rfind(".")
                if dot != -1:
                    title = title[dot + 1 :]
        # if the first character is a dot, search more specific namespaces
        # first else search builtins first
        if target[0:1] == ".":
            target = target[1:]
            refnode["refspecific"] = True
        return title, target
