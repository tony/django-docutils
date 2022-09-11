import inspect

from django.utils.module_loading import import_string
from docutils.parsers.rst import roles

from django_docutils.references.rst.roles import XRefRole

from ..settings import BASED_LIB_RST


def register_based_roles():
    """Register all roles, exists to avoid race conditions / pulling in deps.

    This makes based a lot leaner by making roles explicit and "opt-in".

    Why? Not all django projects want need intersphinx cross-referencing
    or amazon links (which requires bitly and an amazon product api package).
    Let's use a TEMPLATES-style django config::

    BASED_LIB_RST = {
        'roles': {  #: directive-name: Directive class (import string)
            'local': {  #: roles.register_local_role
                # below: same as
                # roles.register_local_role('gh', github_role)
                'gh': 'django_docutils.lib.roles.github.git_role',
                'pypi': 'django_docutils.lib.roles.pypi.pypi_role',
            },
            'canonical': {  #: roles.register_canonical_role
                # below: same as:
                # roles.register_canonical_role('class', PyXRefRole())
                'class': 'django_docutils.lib.roles.xref.PyXRefRole',

                # below: same as
                # roles.register_canonical_role(
                #     'ref',
                #     XRefRole(
                #         lowercase=True, innernodeclass=nodes.inline,
                #         warn_dangling=True
                #     )
                # )
                # See nodes.inline will be resolved
                'ref': (
                    'django_docutils.lib.roles.xref.XRefRole',
                    {
                        'lowercase': True,
                        'innernodeclass': 'docutils.nodes.inline',
                        'warn_dangling': True
                    }
                ),
                'meth': (
                    'django_docutils.lib.roles.xref.PyXRefRole',
                    {
                        'fix_parens': True
                    }
                ),
            }
        }
    }
    """
    if not BASED_LIB_RST:
        return

    if "roles" not in BASED_LIB_RST:
        return

    based_roles = BASED_LIB_RST["roles"]

    local_roles = based_roles.get("local", None)

    if local_roles:
        register_role_mapping(local_roles)


def register_role_mapping(role_mapping):
    """Register a dict mapping of roles

    An item consists of a role name, import string to a callable, and an
    optional mapping of keyword args for special roles that are classes
    that can accept arguments.

    The term inside 'cb' is short for callback/callable. Since the string can
    be any callable object: a function or class.

    :param role_mapping:
    :type role_mapping: dict
    :rtype: void
    :returns: Nothing
    """

    for role_name, role_cb_str in role_mapping.items():
        role_cb_kwargs = {}

        if isinstance(role_cb_str, tuple):
            # (
            #     'django_docutils.lib.roles.xref.PyXRefRole', # role_cb_str
            #     { # role_cb_kwargs
            #         'fix_parens': True
            #     }
            # ),

            # pop off dict of kwargs
            role_cb_kwargs = role_cb_str[1]

            # move class string item to a pure string
            role_cb_str = role_cb_str[0]

            # One more check, we may have an innernodeclass that needs
            # to be resolved, e.g.
            # (
            #     'django_docutils.lib.roles.xref.XRefRole',
            #     {
            #         'lowercase': True,
            #         'innernodeclass': 'docutils.nodes.inline',
            #         'warn_dangling': True
            #     }
            # ),
            if "innernodeclass" in role_cb_kwargs and isinstance(
                role_cb_kwargs["innernodeclass"], str
            ):
                role_cb_kwargs["innernodeclass"] = import_string(
                    role_cb_kwargs["innernodeclass"]
                )

        # Docutils roles accept a function or callable class as a callback
        role_ = import_string(role_cb_str)

        # Stuff like cross-reference roles, which are derived from sphinx work
        # differently. Unlike normal function roles, these roles are classes
        # passed in instantiated.
        #
        # If they include kwargs, they are entered as a tuple with a second
        # element that's a dict of the kwargs passed into the role.
        if inspect.isclass(role_) and issubclass(role_, XRefRole):
            if role_cb_kwargs:
                roles.register_local_role(role_name, role_(**role_cb_kwargs))
            else:
                roles.register_local_role(role_name, role_())
        else:
            roles.register_local_role(role_name, role_)
