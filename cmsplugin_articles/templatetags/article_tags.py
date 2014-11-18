from django import template
register = template.Library()


@register.filter()
def article_title(article_page):
    return article_page.get_title()
