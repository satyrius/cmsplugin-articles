==================
cmsplugin-articles
==================
.. image:: https://travis-ci.org/satyrius/cmsplugin-articles.svg?branch=master
  :target: https://travis-ci.org/satyrius/cmsplugin-articles

It is a simple plugin that allows you to organize you article pages in a manner of a blog.
It does not break original page publishing workflow, but has some tricks to gather articles into a blog app.

Requirements
============

It works fine and tested under ``Python 2.7``. The following libraries are required

- ``Django`` 1.5 or 1.6
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

Customization
=============

You can customize this plugin by overriding the following templates

- ``cms/plugins/articles.html`` (plugin template layout)
- ``cms/plugins/article_teaser.html`` (if you want to change teaser template, e.g. use `easy-thumbnails` for teaser images)
- ``cms/plugins/articles_pagination.html`` (pagination templates, if you want to add extra css classes or so)


Roadmap
=======
- Translations
- Django 1.7 and Python 3 support

Usage
=====

- Create a page in a common way, it will be a root page, an articles list;
- Add ``ArticlesPlugin`` to the page to you content placeholder, this will show a list of published articles;
- Create an article page as a child page, it will be shown automatocally in the list.

Changelog
=========
The changelog can be found at `repo's release notes <https://github.com/satyrius/cmsplugin-articles/releases>`_

Contributing
============
Fork the repo, create a feature branch then send me pull request. Feel free to create new issues or contact me via email.
