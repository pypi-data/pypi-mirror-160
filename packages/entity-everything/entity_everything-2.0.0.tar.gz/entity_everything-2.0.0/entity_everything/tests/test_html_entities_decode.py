from unittest import TestCase
from entity_everything.lib import html_entities_decode


class TestHtmlEntitiesDecode(TestCase):
    def test_html_entities_decode_for_empty_strings(self):
        assert html_entities_decode("") == ""

    def test_html_entities_encode_for_emojis(self):
        assert html_entities_decode("&#128517;&#128142;&#128519;") == "😅💎😇"

    def test_html_entities_encode_for_text(self):
        to_decode = "&#120;&#120;&#120;&#32;&#108;&#111;&#114;&#101;&#109;" \
                   "&#32;&#105;&#112;&#115;&#117;&#109;&#32;&#120;&#120;&#120;"
        assert html_entities_decode(to_decode) == "xxx lorem ipsum xxx"
