"""SEO tests: meta tags, robots.txt, sitemap.xml."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as A


class SeoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        A.app.testing = True
        cls.client = A.app.test_client()

    def test_home_has_seo_tags(self):
        body = self.client.get("/").get_data(as_text=True)
        for tag in ['name="description"', 'rel="canonical"', 'og:title',
                    'og:description', 'twitter:card', 'application/ld+json',
                    'name="robots"']:
            self.assertIn(tag, body, f"missing: {tag}")

    def test_pages_have_unique_descriptions(self):
        descs = set()
        for path in ["/", "/tools", "/tutorials", "/blog", "/about", "/contact"]:
            body = self.client.get(path).get_data(as_text=True)
            self.assertIn('name="description"', body, path)
            start = body.index('name="description" content="') + len('name="description" content="')
            descs.add(body[start:body.index('"', start)])
        self.assertGreater(len(descs), 1, "pages should have distinct descriptions")

    def test_robots_txt(self):
        r = self.client.get("/robots.txt")
        self.assertEqual(r.status_code, 200)
        body = r.get_data(as_text=True)
        self.assertIn("User-agent:", body)
        self.assertIn("Sitemap:", body)
        self.assertIn("sitemap.xml", body)

    def test_sitemap_xml(self):
        r = self.client.get("/sitemap.xml")
        self.assertEqual(r.status_code, 200)
        body = r.get_data(as_text=True)
        self.assertIn("<urlset", body)
        for url in ["/tools", "/tutorials", "/blog", "/about", "/contact"]:
            self.assertIn(url, body)


if __name__ == "__main__":
    unittest.main()
