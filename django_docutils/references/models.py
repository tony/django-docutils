from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import gettext_lazy as _


def get_reference_model():
    try:
        return django_apps.get_model(
            settings.BASED_REFERENCE_MODEL, require_ready=False
        )
    except ValueError:
        raise ImproperlyConfigured(
            "BASED_REFERENCE_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "BASED_REFERENCE_MODEL refers to model '%s' that has not been installed"
            % settings.BASED_REFERENCE_MODEL
        )


class ReferenceBase(models.Model):

    r"""Reference for targets, including the intersphinx network.

    :py:mod:`py3k:module2`
     |   |         |
     |   |         ---- target
     |   -- type          |
     |-- domain      py3k:module2
                       |    |
             setname --|    |-- settarget

    An intersphinx collection can link to a "set", or a remote manifest of
    many references, such as in Python, Sphinx, or SQLAlchemy's documentation.

    While vanilla docutils only has targets for its local documents, sphinx
    creates a manifest of targets project-wide. It collects these in an
    "inventory", which we namespace through : in the "target", e.g.
    "py3k:collections", where py3k is the namespace INTERSPHINX_MAPPING pointed
    to python 3's documentation on the internet. e.g.:

    intersphinx_mapping = {
        'https://docs.python.org/': inv_file,
        'py3k': ('https://docs.python.org/py3k/', inv_file),
    }

    See how there's also an item with setname (docs.python.org, the first
    entry). Sphinx allows this, so items which don't show a setname for the
    target (e.g. "collections", without the "py3k:" namespace) will refer to
    targets in https://docs.python.org instead of https://docs.python.org/py3k/

    Note: intersphinx represents the nameless inventory to be the "main
    inventory". And the others as "name inventories".

    Also of note is the domain and type, e.g. (:py:mod:). By default, sphinx
    uses the python domain, so you could actually do :mod: without the :py:.
    e.g. \:mod\:`collections` instead of \:py\:mod\:`collections`.

    However, it's still important to store and collect the domain and type,
    since we'll want to reference multiple programming languages. In addition,
    despite the practice of intersphinx_mapping to have a default set with no
    set name, and a default fallback domain, it may be more correct in the long
    term to enforce explicit domains and sets.
    """

    domain = models.CharField(
        _('Sphinx domain of the reference. e.g. "py" or "std"'), max_length=255
    )
    type = models.CharField(
        _('Type of object being linked to, e.g. "mod", "func", "option"'),
        max_length=255,
    )
    project = models.CharField(
        _("Project, e.g. py3k, python, sqlalchemy"), max_length=255
    )
    project_version = models.CharField(
        _("Version of project documentation"), max_length=255
    )
    target = models.CharField(_("Docutils/Sphinx target"), max_length=255)
    uri = models.URLField(_("Link to reference"), max_length=255)
    display_name = models.CharField(
        _("Optional name for the reference item"), max_length=255, null=True
    )

    @property
    def full_target(self):
        return f"{self.project}:{self.target}"

    @property
    def full_reference(self):
        if self.domain:
            return ":{}:{}:`{}:{}`".format(
                self.domain, self.type, self.project, self.full_target
            )
        else:
            return f":{self.type}:`{self.target}`"

    class Meta:
        unique_together = ("project", "target", "type")
        abstract = True

    def __str__(self):
        return self.full_reference
