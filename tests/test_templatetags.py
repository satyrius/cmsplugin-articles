import base64
import datetime as dt
import unittest

from bs4 import BeautifulSoup
from cms.api import create_page, add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template import Template, Context
from freezegun import freeze_time

from cmsplugin_articles.models import TeaserExtension
from cmsplugin_articles.templatetags.article_tags import exact_columns
from cmsplugin_articles import settings


class TemplatetagsTest(CMSTestCase):
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
        title = 'Ajani, Mentor of Heroes'
        page = self._create_page(title)
        res = self._render('{{ page|teaser_title }}', page=page).strip()
        self.assertEqual(res, title)

        short_title = 'Ajani'
        TeaserExtension.objects.create(
            extended_object=page,
            title=short_title)
        res = self._render('{{ page|teaser_title }}', page=page).strip()
        self.assertEqual(res, short_title)

    @freeze_time('2008-09-02')
    def test_published_at(self):
        page = self._create_page('Wild Nacatl')
        template = '{{ page|published_at|date:"Y-m-d" }}'

        self.assertIsNotNone(page.creation_date)
        self.assertIsNone(page.publication_date)
        res = self._render(template, page=page).strip()
        self.assertEqual(res, '2008-09-02')

        page.publication_date = page.creation_date + dt.timedelta(days=1)
        page.save()
        res = self._render(template, page=page).strip()
        self.assertEqual(res, '2008-09-03')

    def test_teaser_image(self):
        page = self._create_page('Satyrius')
        template = '''
            {% with page|teaser_image as img %}
                {{ img.url }}
            {% endwith %}
        '''
        res = self._render(template, page=page).strip()
        self.assertEqual(res, '')

        content = base64.decodestring(IMAGE)
        img = SimpleUploadedFile('me.jpeg', content, content_type='image/jpeg')
        teaser = TeaserExtension.objects.create(
            extended_object=page, image=img)

        res = self._render(template, page=page).strip()
        self.assertEqual(res, teaser.image.url)

    def test_teaser_text(self):
        request = self.get_request(language='en')

        page = self._create_page('Green Sun\'s Zenith')
        placeholder = page.placeholders.create(slot='body')
        text = '<p>Search your library for a green creature card with ' \
               'converted mana cost X or less, put it onto the battlefield, ' \
               'then shuffle your library. Shuffle Green Sun\'s Zenith into ' \
               'its owner\'s library.</p>'
        plugin = add_plugin(placeholder, 'TextPlugin', 'en', body=text)
        self.assertEqual(plugin.placeholder, placeholder)

        template = '{% teaser_text page %}'
        res = self._render(template, page=page).strip()
        self.assertEqual(res, '')

        # Render default teaser text using page "body" placeholder
        template2 = '{% teaser_text page "body" %}'
        settings.TEASER_CUT = 10
        res = self._render(template2, page=page, request=request).strip()
        self.assertEqual(res, 'Search you...')

        flavor = 'As the green sun crowned, Phyrexian prophecies glowed on ' \
                 'the Tree of Tales.'
        TeaserExtension.objects.create(
            extended_object=page, description=flavor)

        res = self._render(template, page=page).strip()
        self.assertEqual(res, flavor)

    def test_exact_columns_vertical(self):
        lst = [1, 2, 3, 4]
        template = '''
            {% exact_columns values 3 as columns %}
            {% for column in columns %}
                <div class="col">
                    {% for item in column %}
                        <div class="item">{{ item }}</div>
                    {% endfor %}
                </div>
            {% endfor %}
        '''
        html = self._render(template, values=lst)
        soup = BeautifulSoup(html, 'html.parser')
        cols = soup.select('.col')

        def get_items(col):
            return [int(i.string) for i in col.select('.item')]

        self.assertEqual(get_items(cols[0]), [1, 2])
        self.assertEqual(get_items(cols[1]), [3])
        self.assertEqual(get_items(cols[2]), [4])

    def test_exact_columns_horizontal(self):
        lst = [1, 2, 3, 4]
        template = '''
            {% exact_columns values 3 "horizontal" as columns %}
            {% for column in columns %}
                <div class="col">
                    {% for item in column %}
                        <div class="item">{{ item }}</div>
                    {% endfor %}
                </div>
            {% endfor %}
        '''
        html = self._render(template, values=lst)
        soup = BeautifulSoup(html, 'html.parser')
        cols = soup.select('.col')

        def get_items(col):
            return [int(i.string) for i in col.select('.item')]

        self.assertEqual(get_items(cols[0]), [1, 4])
        self.assertEqual(get_items(cols[1]), [2])
        self.assertEqual(get_items(cols[2]), [3])


class ColumnsLayoutTest(unittest.TestCase):
    def test_exact_columns_vertical_even(self):
        self.assertEqual(
            exact_columns([1, 2, 3, 4, 5, 6, 7, 8], 2, mode='vertical'),
            [[1, 2, 3, 4], [5, 6, 7, 8]])

    def test_exact_columns_vertical_not_enough_elements(self):
        self.assertEqual(
            exact_columns([1, 2], 3, mode='vertical'),
            [[1], [2], []])

    def test_exact_columns_vertical_justify(self):
        self.assertEqual(
            exact_columns([1, 2, 3, 4, 5, 6, 7, 8], 3, mode='vertical'),
            [[1, 2, 3], [4, 5, 6], [7, 8]])

        self.assertEqual(
            exact_columns([1, 2, 3, 4, 5, 6, 7, 8, 9], 4, mode='vertical'),
            [[1, 2, 3], [4, 5], [6, 7], [8, 9]])

        self.assertEqual(
            exact_columns([1, 2, 3, 4, 5], 4, mode='vertical'),
            [[1, 2], [3], [4], [5]])

        self.assertEqual(
            exact_columns([1, 2, 3, 4], 3, mode='vertical'),
            [[1, 2], [3], [4]])

    def test_exact_columns_horizontal(self):
        self.assertEqual(
            exact_columns([1, 2, 3, 4, 5, 6, 7, 8], 3, mode='horizontal'),
            [[1, 4, 7], [2, 5, 8], [3, 6]])

        self.assertEqual(
            exact_columns([1, 2, 3, 4], 3, mode='horizontal'),
            [[1, 4], [2], [3]])

        self.assertEqual(
            exact_columns([1, 2], 3, mode='horizontal'),
            [[1], [2], []])


IMAGE = \
    r'/9j/4AAQSkZJRgABAQAAAQABAAD//gA7Q1JFQVRPUjogZ2QtanBlZyB2MS4wICh1c2luZy' \
    r'BJSkcgSlBFRyB2ODApLCBxdWFsaXR5ID0gOTAK/9sAQwADAgIDAgIDAwMDBAMDBAUIBQUE' \
    r'BAUKBwcGCAwKDAwLCgsLDQ4SEA0OEQ4LCxAWEBETFBUVFQwPFxgWFBgSFBUU/9sAQwEDBA' \
    r'QFBAUJBQUJFA0LDRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQU' \
    r'FBQUFBQUFBQU/8AAEQgAFAAUAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAg' \
    r'MEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGh' \
    r'CCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZG' \
    r'VmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TF' \
    r'xsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAA' \
    r'AAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXET' \
    r'IjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVV' \
    r'ZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2' \
    r't7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD' \
    r'8A39WuksNLlvLh/wB1FbGRyeqhRmqOtwatoWn+HtU1NdPk0vXwFt/schZ7eRhlVcng5X07' \
    r'hvTnnPi5rMf2CHSYvMdZpRHdGLGUTOQPfOBx6VnfEDWNcg8B+CrzxB4Z/sFrp5bpbl4Ykl' \
    r'LLgIgZAMIfPcqrHccHPqfGr1ZQkktj5nh7IKGMwVati4+9Je5vp5/N2+SPSHV02quAAPSi' \
    r'o9Ov4tUsobuLd5UyK67hyAVBwfeivQSPy2ScG4yWqPLbm+eTXNdmlSOY+RO+2Rcrn9+P5A' \
    r'D8Km8GfEPWviv4R0DQPEs6X+naTpty0CmMBmZfOVGc/wARVY0A9h6kmiim0nufvOGbjSgo' \
    r'6aL8kdj8PG3aA0eAEhneJAOyjGBRRRQfj2bJLH1v8T/Q/9k='
