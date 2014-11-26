from bs4 import BeautifulSoup
from cms.test_utils.testcases import CMSTestCase
from cms.api import create_page, add_plugin
from django.template import RequestContext


class PluginTest(CMSTestCase):
    def _create_page(self, title, **kwargs):
        data = {
            'title': title,
            'template': 'dummy.html',
            'language': 'en',
            'published': True,
        }
        data.update(kwargs)
        return create_page(**data)

    def _create_blog(self, title, limit=10, **kwargs):
        page = self._create_page(title, **kwargs)
        placeholder = page.placeholders.create(slot='body')
        add_plugin(placeholder, 'ArticlesPlugin', 'en', limit=limit)
        return page, placeholder

    def _render(self, placeholder, page_num=None):
        request = self.get_request(
            language='en',
            page=placeholder.page.reload())
        if page_num is not None:
            request.GET._mutable = True
            request.GET['page'] = str(page_num)
            request.GET._mutable = False
        request_context = RequestContext(request)
        return placeholder.render(request_context, None)

    def _get_titles(self, placeholder, page_num=None):
        html = self._render(placeholder, page_num=page_num)
        soup = BeautifulSoup(html, 'html.parser')
        return {h.string for h in soup.find_all('h2')}

    def test_articles(self):
        blog1, body = self._create_blog('Blog 1')
        self._create_page('Article 1', parent=blog1)
        self._create_page('Article 2', parent=blog1)
        self.assertEqual(len(blog1.reload().get_children()), 2)

        blog2, _ = self._create_blog('Blog 2')
        self._create_page('Article 3', parent=blog2)
        self.assertEqual(len(blog2.reload().get_children()), 1)

        titles = self._get_titles(body)
        self.assertEqual(titles, {'Article 1', 'Article 2'})

    def test_page_limit(self):
        blog1, body = self._create_blog('Blog 1', limit=2)
        self._create_page('Article 1', parent=blog1)
        self._create_page('Article 2', parent=blog1)
        self._create_page('Article 3', parent=blog1)

        # Assert two latest articles on the first page
        titles = self._get_titles(body, page_num=1)
        self.assertEqual(titles, {'Article 2', 'Article 3'})

        # And the oldest particle on the second page
        titles = self._get_titles(body, page_num=2)
        self.assertEqual(titles, {'Article 1'})
