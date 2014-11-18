from django import template
register = template.Library()


@register.filter()
def article_title(article_page):
    return article_page.get_title()


@register.filter()
def published_at(article_page):
    return article_page.publication_date or article_page.creation_date
