from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _

from .models import ArticlesPlugin as Plugin


class ArticlesPlugin(CMSPluginBase):
    model = Plugin
    name = _('Articles Plugin')
    render_template = 'cms/plugins/articles.html'

    def get_articles_paginator(self, request, instance):
        articles = request.current_page.get_children().order_by(
            '-creation_date')
        return self.get_paginator(request, articles, instance.limit)

    def get_page_number(self, request):
        try:
            return int(request.GET.get('page', 1))
        except ValueError:
            return 1

    def get_article_data(self, page):
        data = {
            'title': page.get_title,
            'published_at': page.publication_date or page.creation_date,
        }
        return data

    def render(self, context, instance, placeholder):
        request = context['request']
        paginator = self.get_articles_paginator(request, instance)
        page = paginator.page(self.get_page_number(request))
        articles = [
            self.get_article_data(article)
            for article in page.object_list
        ]
        context.update({
            'instance': instance,
            'paginator': paginator,
            'page_obj': page,
            'articles': articles,
        })
        return context

plugin_pool.register_plugin(ArticlesPlugin)
