from bs4 import BeautifulSoup
from cms.models import Placeholder
from django import template
from django.template import RequestContext
from cmsplugin_articles.models import TeaserExtension
from cmsplugin_articles import settings

register = template.Library()


@register.filter()
def published_at(article_page):
    return article_page.publication_date or article_page.creation_date


@register.filter()
def teaser_title(article_page):
    try:
        teaser = article_page.teaserextension
    except TeaserExtension.DoesNotExist:
        pass
    else:
        if teaser.title:
            return teaser.title
    return article_page.get_title()


@register.filter()
def teaser_image(article_page):
    try:
        teaser = article_page.teaserextension
    except TeaserExtension.DoesNotExist:
        pass
    else:
        return teaser.image
    return None


@register.simple_tag(takes_context=True)
def teaser_text(context, article_page, default_from=None):
    try:
        teaser = article_page.teaserextension
    except TeaserExtension.DoesNotExist:
        if default_from:
            try:
                placeholder = article_page.placeholders.get(slot=default_from)
            except Placeholder.DoesNotExist:
                pass
            else:
                request_context = RequestContext(context['request'])
                html = placeholder.render(request_context, None)
                soup = BeautifulSoup(html, 'html.parser')
                paragraphs = u' '.join([
                    unicode(p.string) for p in soup.find_all('p')])
                cut = paragraphs[:settings.TEASER_CUT]
                if cut:
                    return cut + u'...'
    else:
        return teaser.description
    return u''
