from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _

from .models import ArticlesPlugin as Plugin


class ArticlesPlugin(CMSPluginBase):
    model = Plugin
    name = _('Articles Plugin')
    render_template = 'cms/plugins/articles.html'

    def get_articles(self, request):
        return request.current_page.get_children().order_by('-creation_date')

    def get_article_data(self, page):
        data = {
            'title': page.get_title,
            'published_at': page.publication_date or page.creation_date,
        }
        return data

    def render(self, context, instance, placeholder):
        articles = [
            self.get_article_data(page)
            for page in self.get_articles(context['request'])
        ]
        context.update({
            'instance': instance,
            'articles': articles,
        })
        return context

plugin_pool.register_plugin(ArticlesPlugin)
