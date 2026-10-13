import unittest
from services.parser import parse_quotes, next_page_url


SAMPLE = """
<html><body>
<div class="quote">
 <span class="text">“Practice makes progress.”</span>
 <small class="author">Test Author</small>
 <div class="tags"><a class="tag">learning</a><a class="tag">python</a></div>
</div>
<ul class="pager"><li class="next"><a href="/page/2/">Next</a></li></ul>
</body></html>
"""


class ParserTests(unittest.TestCase):
    def test_parse_quote_fields(self):
        quotes = parse_quotes(SAMPLE, "https://example.com/")
        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0].text, "Practice makes progress.")
        self.assertEqual(quotes[0].author, "Test Author")
        self.assertEqual(quotes[0].tags, ["learning", "python"])

    def test_next_page_url(self):
        result = next_page_url(SAMPLE, "https://example.com/")
        self.assertEqual(result, "https://example.com/page/2/")


if __name__ == "__main__":
    unittest.main()
