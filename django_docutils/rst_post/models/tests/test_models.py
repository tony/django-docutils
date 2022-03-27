import pytest

from django.core import checks
from django.db import models

from django_docutils.favicon.tests.test_app.models import RSTPost, RSTPostSubclass
from django_docutils.rst_post.models import (
    RSTPostBase,
    RSTPostPageBase,
    get_post_models,
)


def test_get_post_models():
    models = get_post_models()
    assert RSTPost in models
    assert RSTPostSubclass not in models


def test_no_root_page_field():
    class NoRootPage(RSTPostBase):
        class Meta:
            app_label = "test"

    assert NoRootPage.check() == [
        checks.Error(
            "Missing root_page field.",
            hint="Add a root_page ForeignKey a subclass of RSTPostPageBase",
            obj=NoRootPage,
            id="rst_post.E001",
        )
    ]


def test_root_page_wrong_field_type():
    class WrongRootPageFieldType(RSTPostBase):
        root_page = models.CharField(max_length=255)

        class Meta:
            app_label = "test"

    assert WrongRootPageFieldType.check() == [
        checks.Error(
            "Wrong field type for root_page field.",
            hint="Use a models.ForeignKey field.",
            obj=WrongRootPageFieldType,
            id="rst_post.E002",
        )
    ]


@pytest.mark.django_db
def test_root_page_wrong_relation(EmptyModel):
    class WrongRootPageRelation(RSTPostBase):
        root_page = models.ForeignKey(EmptyModel, on_delete=models.CASCADE)

        class Meta:
            app_label = "test"

    assert WrongRootPageRelation.check() == [
        checks.Error(
            "Wrong related model for root_page relationship.",
            hint="Use a model subclassing RSTPostPageBase",
            obj=WrongRootPageRelation,
            id="rst_post.E003",
        )
    ]


@pytest.mark.django_db
def test_postpage_back_relation_no_field(transactional_db):
    class NoPageRelation(RSTPostPageBase):
        class Meta:
            app_label = "test"

    assert NoPageRelation.check() == [
        checks.Error(
            "Missing post field.",
            hint="Add a post ForeignKey that subclasses RSTPostBase",
            obj=NoPageRelation,
            id="rst_post.E004",
        )
    ]


@pytest.mark.django_db
def test_postpage_back_relation_field_type():
    class WrongPageFieldType(RSTPostPageBase):
        post = models.CharField(max_length=255)

        class Meta:
            app_label = "test"

    assert WrongPageFieldType.check() == [
        checks.Error(
            "Wrong field type for post field.",
            hint="Use a models.ForeignKey field.",
            obj=WrongPageFieldType,
            id="rst_post.E005",
        )
    ]


@pytest.mark.django_db
def test_postpage_back_relation_relation_type(EmptyModel):
    class WrongPostBackRelation(RSTPostPageBase):
        post = models.ForeignKey(EmptyModel, on_delete=models.CASCADE)

        class Meta:
            app_label = "test"

    assert WrongPostBackRelation.check() == [
        checks.Error(
            "Wrong related model for post relationship.",
            hint="Use a model subclassing RSTPostBase",
            obj=WrongPostBackRelation,
            id="rst_post.E006",
        )
    ]
