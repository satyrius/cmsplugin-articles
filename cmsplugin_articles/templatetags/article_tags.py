from django import template
from cmsplugin_articles.models import TeaserExtension

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
