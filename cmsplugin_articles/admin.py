from django.contrib import admin
from cms.extensions import PageExtensionAdmin

from .models import TeaserExtension


class TeaserExtensionAdmin(PageExtensionAdmin):
    pass

admin.site.register(TeaserExtension, TeaserExtensionAdmin)
