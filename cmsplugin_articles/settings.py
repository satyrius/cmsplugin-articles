from django.conf import settings


# Number of articles per page
PAGINATE_BY = getattr(settings, 'CMS_ARTICLES_PAGINATE_BY', 10)

# Text length for auto teaser
TEASER_CUT = getattr(settings, 'CMS_ARTICLES_TEASER_CUT', 200)
