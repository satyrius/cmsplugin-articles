from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ListPlugin(CMSPlugin):
    limit = models.PositiveIntegerField(_('Articles per page'))
