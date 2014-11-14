import re
from bs4 import BeautifulSoup
from cms.models import Placeholder
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.template import RequestContext
from django.utils.translation import ugettext as _


from . import settings
from .models import ArticlesPlugin as Plugin, TeaserExtension


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

    def get_article_data(self, page, request):
        request_context = RequestContext(request)
        data = {
            'title': page.get_title(),
            'published_at': page.publication_date or page.creation_date,
            'image': None,
            'teaser': '<!-- no content -->',
        }
        more = u'<a href="{u}">more</a>'.format(u=page.get_absolute_url())

        try:
            teaser = page.teaserextension
        except TeaserExtension.DoesNotExist:
            teaser = None
        else:
            data['image'] = teaser.image
            # TODO quote description text
            data['teaser'] = u'<p>{t} {u}</p>'.format(
                t=teaser.description or '', u=more)
            if teaser.title:
                data['title'] = teaser.title

        if not teaser:
            try:
                content = page.placeholders.get(slot='content')
            except Placeholder.DoesNotExist:
                pass
            else:
                # TODO Move this out from view class (e.g. to templatetags)
                soup = BeautifulSoup(
                    content.render(request_context, None),
                    'html.parser')
                paragraphs = u''.join([
                    unicode(p.string) for p in soup.find_all('p')])
                cut = re.sub(
                    r'<(?:/(?:\w+)?)?$', '',
                    paragraphs[:settings.TEASER_CUT]) + u'... ' + more
                data['teaser'] = unicode(BeautifulSoup(cut, 'html.parser'))
                # Look for article headers
                headers = soup.find_all('h1', limit=1)
                headers.extend(soup.find_all('h2', limit=1))
                headers.extend(soup.find_all('h3', limit=1))
                if headers:
                    data['title'] = headers[0].getText()

        return data

    def render(self, context, instance, placeholder):
        request = context['request']
        paginator = self.get_articles_paginator(request, instance)
        page = paginator.page(self.get_page_number(request))
        articles = [
            self.get_article_data(article, request)
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
