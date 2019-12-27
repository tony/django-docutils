from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse


def get_taxonomy_model(model_key):
    """
    Example:

    .. code-block:: python

        BASED_TAXONOMY_MODELS = {  #: URL namespace/RST role -> app_label:model_name
            'platforms': 'taxonomy.Platform',
            'programming_languages': 'taxonomy.ProgrammingLanguage',
            'topics': 'taxonomy.Topic',
        }
    """
    MODELS = getattr(settings, 'BASED_TAXONOMY_MODELS', {})
    try:
        return django_apps.get_model(MODELS.get(model_key), require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"BASED_TAXONOMY_MODELS['{model_key}'] must be of the form "
            "'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"BASED_TAXONOMY_MODELS['{model_key}'] refers to model '%s' that has not "
            "been installed" % MODELS.get(model_key)
        )


def get_taxonomy_models():
    """Return mapping of model objects (lazily-loaded)"""
    MODELS = getattr(settings, 'BASED_TAXONOMY_MODELS', {})
    return {k: get_taxonomy_model(k) for k, v in MODELS.items()}


def get_absolute_url_from_namespace(tag, namespace):
    key = tag._meta.verbose_name_plural.title()  # e.g. 'topics'
    return reverse('%s:list-view' % namespace, kwargs={key: slugify(tag.title)})
