import dirtyfields
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import (
    AutoSlugField,
    CreationDateTimeField,
    ModificationDateTimeField,
)
from django_slugify_processor.text import slugify
from randomslugfield import RandomSlugField


def get_post_model():
    try:
        return django_apps.get_model(settings.BASED_POST_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "BASED_POST_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "BASED_POST_MODEL refers to model '%s' that has not been installed"
            % settings.BASED_POST_MODEL
        )


def get_post_models():
    """Return high-level PageBase models. Skips subclasses of PostBase."""
    models = []
    for model in django_apps.get_models():
        if issubclass(model, RSTPostBase) and model.__subclasses__():
            models.append(model)
    return models


def get_anonymous_user_instance(UserModel=None):
    if UserModel is None:
        from django.contrib.auth import get_user_model

        UserModel = get_user_model()
    user, _ = UserModel.objects.get_or_create(
        username=settings.ANONYMOUS_USER_NAME, email="noone@localhost"
    )
    return user


class RSTPostBase(dirtyfields.DirtyFieldsMixin, models.Model):
    title = models.CharField(_("title"), max_length=255)

    slug_title = AutoSlugField(
        _("slug"), populate_from="title", slugify_function=slugify
    )

    slug_id = RandomSlugField(length=8, unique=True, editable=False)
    author_name = models.CharField(_("Author name"), max_length=255)
    is_draft = models.BooleanField(default=False, editable=False, db_index=True)
    created = CreationDateTimeField(_("created"))
    modified = ModificationDateTimeField(_("modified"))

    class Meta:
        ordering = ["-created"]
        abstract = True

    def save(self, **kwargs):
        self.update_modified = kwargs.pop(
            "update_modified", getattr(self, "update_modified", True)
        )
        super().save(**kwargs)

    @cached_property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    @cached_property
    def subtitle(self):
        return self.root_page.subtitle

    def __str__(self):
        title = self.title
        if self.subtitle:
            title += ": " + self.subtitle
        return title

    @classmethod
    def check(cls, **kwargs):
        from .checks import _check_root_page

        errors = super().check(**kwargs)
        errors.extend(_check_root_page(cls))
        return errors
