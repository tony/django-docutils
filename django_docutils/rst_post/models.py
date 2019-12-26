import dirtyfields
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core import checks
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.db import models
from django.db.models.fields.related import resolve_relation
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import (
    AutoSlugField,
    CreationDateTimeField,
    ModificationDateTimeField,
)
from django_slugify_processor.text import slugify
from randomslugfield import RandomSlugField

from django_docutils.lib.publisher import publish_doctree


def get_anonymous_user_instance(UserModel=get_user_model()):
    user, _ = UserModel.objects.get_or_create(
        username=settings.ANONYMOUS_USER_NAME, email='noone@localhost'
    )
    return user


def _check_root_page(cls):
    """System check for root_page field on PostBase models."""
    try:
        root_page = cls._meta.get_field('root_page')

        # must be correct field type
        if root_page.__class__ != models.ForeignKey:
            return [
                checks.Error(
                    'Wrong field type for root_page field.',
                    hint='Use a models.ForeignKey field.',
                    obj=cls,
                    id='rst_post.E002',
                )
            ]
        else:  # check for the correct relation inside root_page
            # incase of model class import strings, e.g. 'MyPostPage'
            # instead of MyPostPage
            related_model = resolve_relation(cls, root_page.related_model)
            if not issubclass(related_model, RSTPostPageBase):
                return [
                    checks.Error(
                        'Wrong related model for root_page relationship.',
                        hint='Use a model subclassing RSTPostPageBase',
                        obj=cls,
                        id='rst_post.E003',
                    )
                ]
    except FieldDoesNotExist:  # no root_page field
        return [
            checks.Error(
                'Missing root_page field.',
                hint='Add a root_page ForeignKey a subclass of RSTPostPageBase',
                obj=cls,
                id='rst_post.E001',
            )
        ]
    return []


def _check_postpage_post_back_relation(cls):
    """System check for post field on PostPageBase models."""
    try:
        page_field = cls._meta.get_field('post')

        # must be correct field type
        if page_field.__class__ != models.ForeignKey:
            return [
                checks.Error(
                    'Wrong field type for post field.',
                    hint='Use a models.ForeignKey field.',
                    obj=cls,
                    id='rst_post.E005',
                )
            ]
        else:  # check for the correct relation inside page_field
            # incase of model class import strings, e.g. 'MyPostPage'
            # instead of MyPostPage
            related_model = resolve_relation(cls, page_field.related_model)
            if not issubclass(related_model, RSTPostBase):
                return [
                    checks.Error(
                        'Wrong related model for post relationship.',
                        hint='Use a model subclassing RSTPostBase',
                        obj=cls,
                        id='rst_post.E006',
                    )
                ]
    except FieldDoesNotExist:  # no page_field field
        return [
            checks.Error(
                'Missing post field.',
                hint='Add a post ForeignKey that subclasses PostBase',
                obj=cls,
                id='rst_post.E004',
            )
        ]
    return []


class RSTPostBase(dirtyfields.DirtyFieldsMixin, models.Model):
    title = models.CharField(_('title'), max_length=255)

    slug_title = AutoSlugField(
        _('slug'), populate_from='title', slugify_function=slugify
    )

    slug_id = RandomSlugField(length=8, unique=True, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET(get_anonymous_user_instance)
    )
    is_draft = models.BooleanField(default=False, editable=False, db_index=True)
    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'))

    class Meta:
        ordering = ['-created']
        abstract = True

    def save(self, **kwargs):
        self.update_modified = kwargs.pop(
            'update_modified', getattr(self, 'update_modified', True)
        )
        super().save(**kwargs)

    def taxonomy_tags(self, taxonomy_field):
        """Used by category_tags template tag to show taxonomies."""
        return getattr(self, taxonomy_field).get_queryset()

    @cached_property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    @cached_property
    def subtitle(self):
        return self.root_page.subtitle

    def __str__(self):
        title = self.title
        if self.subtitle:
            title += ': ' + self.subtitle
        return title

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(_check_root_page(cls))
        return errors


class RSTPostPageBase(models.Model):

    """Where the content of a post resides. Posts can have multiple pages."""

    body = models.TextField()
    subtitle = models.CharField(_('sub title'), max_length=255, null=True, blank=True)
    page_number = models.PositiveSmallIntegerField(null=True)

    class Meta:
        abstract = True

    def __str__(self):
        if self.subtitle:
            return '{title}: {subtitle}'.format(
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
                f'{self.post_url_key}:detail-view',
                kwargs={
                    'slug_id': self.post.slug_id,
                    'slug_title': self.post.slug_title,
                    'page': self.page_number,
                },
            )
        except NoReverseMatch:
            return reverse(
                f'{self.post_url_key}:detail-view',
                kwargs={'slug_title': self.post.slug_title, 'page': self.page_number},
            )

    @cached_property
    def post_url_key(self):
        return self.post.__class__.__name__.lower() + 's'

    def get_edit_url(self):
        try:
            return reverse(
                f'{self.post_url_key}:update-view',
                kwargs={'slug_id': self.post.slug_id, 'page': self.page_number},
            )
        except NoReverseMatch:
            return reverse(
                f'{self.post_url_key}:update-view',
                kwargs={'slug_title': self.post.slug_title, 'page': self.page_number},
            )

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
        errors = super().check(**kwargs)
        errors.extend(_check_postpage_post_back_relation(cls))
        return errors
