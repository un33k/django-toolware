from django.test import TestCase
from django.conf import settings

from ..utils.query import get_text_tokenizer
from ..compat import *


class TestStringTokenizerCase(TestCase):
    """
    Tokenized Test
    """
    def test_tokenizer_test(self):
        text = "This is a test -This -is -NOT -a -test"
        includes, excludes = get_text_tokenizer(text)
        self.assertEquals('-'.join(includes), "This-is-a-test")
        self.assertEquals('-'.join(excludes), "This-is-NOT-a-test")
