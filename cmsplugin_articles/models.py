from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool


class ArticlesPlugin(CMSPlugin):
    limit = models.PositiveIntegerField(_('Articles per page'))


class TeaserExtension(PageExtension):
    title = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    image = models.ImageField(
        _('Image'), upload_to='teaser', blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)

extension_pool.register(TeaserExtension)
