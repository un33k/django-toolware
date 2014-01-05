from django.conf import settings
from django.test import TestCase

from ..utils.query import get_text_tokenizer



class SiteTestCase(TestCase):
    """
    Site objects are created
    """
    def setUp(self):
        self.resp = self.client.get('/admin')

    def test_admin_page(self):
        self.assertEqual(self.resp.status_code, 200)


class TestStringTokenizerCase(TestCase):
    """
    Tokenized Test
    """

    def test_tokenizer_test(self):
        text = "This is a test -This -is -NOT -a -test"
        includes, excludes = get_text_tokenizer(text)
        self.assertEquals('-'.join(includes), "This-is-a-test")
        self.assertEquals('-'.join(excludes), "This-is-NOT-a-test")
