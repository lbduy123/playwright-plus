import unittest
from playwright_plus import open_new_page


class TestOpenNewPage(unittest.TestCase):
    def test_open_new_page(self):
        (browser, context, page) = open_new_page()
        self.assertEqual(browser.browser_type.name, "chromium")
        self.assertEqual(browser.contexts[0], context)
        self.assertEqual(context.pages[0], page)
        self.assertEqual(vars(context._impl_obj)["_options"]["acceptDownloads"], True)
        self.assertEqual(page.url, "about:blank")


if __name__ == "__main__":
    unittest.main()
