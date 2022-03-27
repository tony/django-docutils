from django.db import models

from django_docutils.favicon.models import FaviconBase
from django_docutils.references.models import ReferenceBase
from django_docutils.rst_post.models import RSTPostBase, RSTPostPageBase


class EmptyModel(models.Model):
    pass


class Reference(ReferenceBase):
    pass


class Favicon(FaviconBase):
    pass


class RSTPost(RSTPostBase):
    root_page = models.ForeignKey(
        "RSTPostPage", null=True, on_delete=models.SET_NULL, related_name="+"
    )


class RSTPostSubclass(RSTPost):
    pass


class RSTPostPage(RSTPostPageBase):

    post = models.ForeignKey(
        RSTPost, on_delete=models.CASCADE, related_name="pages", null=True
    )
