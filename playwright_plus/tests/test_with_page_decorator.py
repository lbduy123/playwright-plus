import unittest
from playwright_plus import with_page


class TestWithPageDecorator(unittest.TestCase):
    def test_with_page_decorator(self):
        @with_page()
        def decorated(page=None):
            return page

        page = decorated()
        self.assertEqual(page.url, "about:blank")


if __name__ == "__main__":
    unittest.main()
