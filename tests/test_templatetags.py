from cms.api import create_page
from django.template import Template, Context
from django.test import TestCase
from freezegun import freeze_time


class TemplatetagsTest(TestCase):
    def _create_page(self, title):
        data = {
            'title': title,
            'template': 'dummy.html',
            'language': 'en',
        }
        return create_page(**data)

    def _render(self, template, **context):
        template = '{% load article_tags %}' + template
        return Template(template).render(Context(context))

    def test_article_title(self):
        title = 'Knight of the Reliquary'
        page = self._create_page(title)
        res = self._render('{{ page|article_title }}', page=page).strip()
        self.assertEqual(res, title)

    @freeze_time('2008-09-02')
    def test_published_at(self):
        page = self._create_page('Wild Nacatl')
        self.assertIsNotNone(page.creation_date)
        res = self._render(
            '{{ page|published_at|date:"Y-m-d" }}',
            page=page).strip()
        self.assertEqual(res, '2008-09-02')
