from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import gettext_lazy as _


class BasedFaviconModelValueError(ImproperlyConfigured):
    def __init__(self, *args: object, **kwargs: object) -> None:
        return super().__init__(
            "BASED_FAVICON_MODEL must be of the form 'app_label.model_name'",
            *args,
            **kwargs,
        )


class BasedFaviconModelLookupError(ImproperlyConfigured):
    def __init__(self, model_name: str, *args: object, **kwargs: object) -> None:
        return super().__init__(
            f"BASED_FAVICON_MODEL refers to model '{model_name}' that has not been "
            "installed",
            *args,
            **kwargs,
        )


def get_favicon_model():
    """
    Return the Favicon model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.BASED_FAVICON_MODEL, require_ready=False)
    except ValueError as e:
        raise BasedFaviconModelValueError() from e
    except LookupError as e:
        raise BasedFaviconModelLookupError(settings.BASED_FAVICON_MODEL) from e


class FaviconBase(models.Model):
    domain = models.URLField(verbose_name=_("Domain or subdomain"), unique=True)
    favicon = models.ImageField(
        verbose_name=("Path to icon in static files"),
        upload_to="favicons",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
