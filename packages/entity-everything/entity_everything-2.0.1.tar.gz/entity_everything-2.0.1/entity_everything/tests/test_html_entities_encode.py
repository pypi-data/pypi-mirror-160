from unittest import TestCase
from entity_everything.libs import html_entities_encode, html_entities_decode


class TestHtmlEntitiesEncode(TestCase):
    def test_html_entities_encode_for_empty_strings(self):
        assert html_entities_encode("") == ""

    def test_html_entities_encode_for_emojis(self):
        assert html_entities_encode("😅💎😇") == "&#128517;&#128142;&#128519;"

    def test_html_entities_encode_for_text(self):
        expected = "&#120;&#120;&#120;&#32;&#108;&#111;&#114;&#101;&#109;" \
                   "&#32;&#105;&#112;&#115;&#117;&#109;&#32;&#120;&#120;&#120;"
        assert html_entities_encode("xxx lorem ipsum xxx") == expected

    def test_html_entities_encode_reverse(self):
        tested_str = "xxx hello world 💎"
        after_encoding = html_entities_encode(tested_str)
        after_decoding = html_entities_decode(after_encoding)
        assert after_decoding == tested_str
