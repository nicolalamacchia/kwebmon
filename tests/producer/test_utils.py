import unittest

from kwebmon.producer.utils import get_sites, BadSitesList
from tests import fixture_path


class TestUtils(unittest.TestCase):
    def test_get_sites_bad_json(self):
        with self.assertRaises(BadSitesList):
            get_sites(fixture_path("bad_json_sites.json"))

    def test_get_sites_with_duplicates(self):
        with self.assertRaises(BadSitesList):
            get_sites(fixture_path("sites_with_duplicates.json"))

    def test_get_sites_invalid(self):
        with self.assertRaises(BadSitesList):
            get_sites(fixture_path("invalid_sites.json"))

    def test_get_sites_success(self):
        sites = get_sites(fixture_path("sites.json"))

        self.assertListEqual(sites, [
            {
                "url": "https://example.net",
                "pattern": r"Example D\w+n"
            },
            {
                "url": "https://example.xorg",
                "pattern": "Bad Domain"
            },
            {
                "url": "https://example.org/404",
                "pattern": "Bad Page"
            },
            {
                "url": "https://example.org",
                "pattern": "Bad Content"
            },
            {
                "url": "https://example.com"
            }
        ])


if __name__ == "__main__":
    unittest.main()
