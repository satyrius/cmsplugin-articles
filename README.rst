==================
cmsplugin-articles
==================

It is a simple plugin that allows you to organize you article pages in a manner of a blog. 
It does not break original page publishing workflow, but has some tricks to gather articles into a blog app.

Installation
============

**WARNING this plugin is under development**

::

-e git+https://github.com/satyrius/cmsplugin-articles.git@master#egg=cmsplugin_article

Usage
=====

- Create a page in a common way, it will be a root page, an articles list;
- Add ``ArticlesPlugin`` to the page to you content placeholder, this will show a list of published articles;
- Create an article page as a child page, it will be shown automatocally in the list.
