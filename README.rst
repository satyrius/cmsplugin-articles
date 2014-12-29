==================
cmsplugin-articles
==================

|ci| |pypi| |status|

.. |ci| image:: https://travis-ci.org/satyrius/cmsplugin-articles.svg?branch=master
    :target: https://travis-ci.org/satyrius/cmsplugin-articles

.. |pypi| image:: https://pypip.in/version/cmsplugin-articles/badge.png?text=pypi
    :target: https://pypi.python.org/pypi/cmsplugin-articles/
    :alt: Latest Version

.. |status| image:: https://pypip.in/status/cmsplugin-articles/badge.png
    :target: https://pypi.python.org/pypi/cmsplugin-articles/
    :alt: Development Status

It is a simple plugin that allows you to organize you article pages in a manner of a blog.
It does not break original page publishing workflow, but has some tricks to gather articles into a blog app.

Requirements
============

It works fine and tested under ``Python 2.7``. The following libraries are required

- ``Django`` >= 1.5
- ``django-cms`` >= 3.0 (we recommend to use Django CMS 3.0 and higher, contact us if you need prior CMS versions supports and have some issues)

Installation
============

::

$ pip install cmsplugin-articles

Configure installed apps in your ``settings.py`` ::

  INSTALLED_APPS = [
      # django contrib and django cms apps
      'cmsplugin_articles',
  ]

Migrate your database ::

  django-admin.py migrate cmsplugin_articles

Usage
=====

- Create a page in a common way, it will be a root page, an articles list;
- Add ``ArticlesPlugin`` to the page to you content placeholder, this will show a list of published articles;
- Create an article page as a child page, it will be shown automatocally in the list.

Customization
=============

You can customize this plugin by overriding the following templates

- ``cms/plugins/articles.html`` (plugin template layout)
- ``cms/plugins/article_teaser.html`` (if you want to change teaser template, e.g. use `easy-thumbnails` for teaser images)
- ``cms/plugins/articles_pagination.html`` (pagination templates, if you want to add extra css classes or so)

Templatetags
------------

The plugin has a number of `temlatetags <https://github.com/satyrius/cmsplugin-articles/blob/master/cmsplugin_articles/templatetags/article_tags.py>`_ used for teaser template, you should load them in your template 
with 

::

{% load article_tags %}

published_at, teaser_title and teaser_image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Filters which get article ``Page`` instance as an argument

- ``published_at`` return ``datetime`` object for publication time
- ``teaser_title`` return teaser title as a string
- ``teaser_image`` return ``TeaserExtension.image`` if exists

teaser_text
~~~~~~~~~~~

A ``simple_tag`` which returns a teaser text. It accepts two parameters

- ``article_page`` the page that teaser belongs to
- ``default_from`` the placeholder name. You can pass it if you want generate teasers automaticaly

exact_columns
~~~~~~~~~~~~~

You can use this template tag to split articles list into a column layout, e.g

::

  <div class="row">
    {% exact_columns articles 3 "vertical" as columns %}
    {% for column in columns %}
      <div class="col_6">
        {% for article in column %}
          {% include "cms/plugins/article_teaser.html" %}
        {% endfor %}
      </div>
    {% endfor %}
  </div>

Roadmap
=======
- Python 3 support

Changelog
=========
The changelog can be found at `repo's release notes <https://github.com/satyrius/cmsplugin-articles/releases>`_

Contributing
============
Fork the repo, create a feature branch then send me pull request. Feel free to create new issues or contact me via email.

Translation
-----------
You could also help me to translate `cmsplugin-articles` to your native language `with Transifex <https://www.transifex.com/projects/p/cmsplugin-articles/resource/main/>`_
