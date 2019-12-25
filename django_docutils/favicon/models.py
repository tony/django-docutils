from django.db import models
from django.utils.translation import ugettext_lazy as _


class Favicon(models.Model):
    domain = models.URLField(verbose_name=_('Domain or subdomain'), unique=True)
    favicon = models.ImageField(
        verbose_name=('Path to icon in static files'),
        upload_to='favicons',
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
