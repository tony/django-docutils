from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from django_docutils.lib.publisher import publish_doctree


def get_postpage_models():
    """Return high-level PageBase models. Highest level PostPage."""
    models = []
    for model in apps.get_models():
        if issubclass(model, RSTPostPageBase) and not model.__subclasses__():
            models.append(model)
    return models


class RSTPostPageBase(models.Model):

    """Where the content of a post resides. Posts can have multiple pages."""

    body = models.TextField()
    subtitle = models.CharField(_("sub title"), max_length=255, null=True, blank=True)
    page_number = models.PositiveSmallIntegerField(null=True)

    class Meta:
        abstract = True

    def __str__(self):
        if self.subtitle:
            return "{title}: {subtitle}".format(
                title=self.post.title, subtitle=self.subtitle
            )
        return self.post.title

    @cached_property
    def title(self):
        return self.post.title

    @cached_property
    def previous_page(self):
        try:
            return self.post.pages.get(page_number=self.page_number - 1)
        except ObjectDoesNotExist:
            return None

    @cached_property
    def next_page(self):
        try:
            return self.post.pages.get(page_number=self.page_number + 1)
        except ObjectDoesNotExist:
            return None

    def get_absolute_url(self):
        try:
            return reverse(
                f"{self.post_url_key}:detail-view",
                kwargs={
                    "slug_id": self.post.slug_id,
                    "slug_title": self.post.slug_title,
                    "page": self.page_number,
                },
            )
        except NoReverseMatch:
            return reverse(
                f"{self.post_url_key}:detail-view",
                kwargs={"slug_title": self.post.slug_title, "page": self.page_number},
            )

    @cached_property
    def post_url_key(self):
        return self.post.__class__.__name__.lower() + "s"

    @cached_property
    def document(self):
        """Return page content in a docutils' document

        :rtype: :class:`docutils.nodes.document`
        """
        return publish_doctree(self.body)

    def get_subclass(self):
        return self.post._meta.concrete_model.objects.get_subclass(pk=self.pk)

    @classmethod
    def check(cls, **kwargs):
        from .checks import _check_postpage_post_back_relation

        errors = super().check(**kwargs)
        errors.extend(_check_postpage_post_back_relation(cls))
        return errors
