from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.fields.related import resolve_relation

from .post import RSTPostBase
from .post_page import RSTPostPageBase


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
                hint='Add a post ForeignKey that subclasses RSTPostBase',
                obj=cls,
                id='rst_post.E004',
            )
        ]
    return []
