import unittest

from gn_django.url import utils

class TestUrlUtils(unittest.TestCase):
    """
    Tests for URL util functions
    """

    def test_strip_protocol_http(self):
        url = 'http://www.example.com'
        stripped = utils.strip_protocol(url)
        self.assertEqual('//www.example.com', stripped)

    def test_strip_protocol_https(self):
        url = 'https://www.example.com'
        stripped = utils.strip_protocol(url)
        self.assertEqual('//www.example.com', stripped)

    def test_strip_protocol_relative(self):
        url = '//www.example.com'
        stripped = utils.strip_protocol(url)
        self.assertEqual('//www.example.com', stripped)

    def test_strip_protocol_none(self):
        url = 'www.example.com'
        stripped = utils.strip_protocol(url)
        self.assertEqual('www.example.com', stripped)

    def test_add_protocol(self):
        self.assertEqual('http://www.example.com', utils.add_protocol('www.example.com'))
        self.assertEqual('http://www.example.com', utils.add_protocol('http://www.example.com'))
        self.assertEqual('https://www.example.com', utils.add_protocol('https://www.example.com'))
        self.assertEqual('ftp://www.example.com', utils.add_protocol('ftp://www.example.com'))
        self.assertEqual('https://www.example.com', utils.add_protocol('www.example.com', 'https'))
        self.assertEqual('http://www.example.com', utils.add_protocol('//www.example.com'))

    def test_add_params_to_url_with_no_params(self):
        url = "/a/b/c"
        url_with_params = utils.add_params_to_url(url, foo="bar", baz="woo")
        self.assertEqual("/a/b/c", url_with_params.split('?')[0])
        self.assertTrue("foo=bar" in url_with_params)
        self.assertTrue("baz=woo" in url_with_params)

    def test_add_params_to_url_with_params_already(self):
        url = "/a/b/c?lol=ayyy"
        url_with_params = utils.add_params_to_url(url, foo="bar", baz="woo")
        self.assertEqual("/a/b/c", url_with_params.split('?')[0])
        self.assertTrue("foo=bar" in url_with_params)
        self.assertTrue("baz=woo" in url_with_params)
        self.assertTrue("lol=ayyy" in url_with_params)

    def test_add_params_to_url_param_values_unencoded(self):
        url = "/a/b/c"
        url_with_params = utils.add_params_to_url(url, foo="bar helloo", baz="woo||yo")
        self.assertEqual("/a/b/c", url_with_params.split('?')[0])
        self.assertTrue("foo=bar+helloo" in url_with_params)
        self.assertTrue("baz=woo%7C%7Cyo" in url_with_params)

    def test_add_path_to_url(self):
        url = "/path/to"
        to_add = "a/resource"
        full_url = utils.add_path_to_url(url, to_add)
        self.assertEqual("/path/to/a/resource", full_url)

    def test_add_path_to_url_trailing_slash(self):
        url = "/path/to/"
        to_add = "a/resource"
        full_url = utils.add_path_to_url(url, to_add)
        self.assertEqual("/path/to/a/resource", full_url)

    def test_add_path_to_url_trailing_and_leading_slash(self):
        url = "/path/to/"
        to_add = "/a/resource"
        full_url = utils.add_path_to_url(url, to_add)
        self.assertEqual("/path/to/a/resource", full_url)

    def test_clean_facebook(self):
        expected = 'https://facebook.com/dimitri'
        self.assertEqual(utils.clean_facebook('https://www.facebook.com/dimitri'), expected)
        self.assertEqual(utils.clean_facebook('Www.facebook.com/dimitri'), expected)
        self.assertEqual(utils.clean_facebook('https://facebook.com/dimitri'), expected)
        self.assertEqual(utils.clean_facebook('facebook.com/dimitri'), expected)
        self.assertEqual(utils.clean_facebook('Facebook.com/dimitri'), expected)
        self.assertEqual(utils.clean_facebook('@dimitri'), expected)
        self.assertEqual(utils.clean_facebook('dimitri'), expected)
        self.assertEqual(utils.clean_facebook('https://www.facebook.com/profile.php?id=dimitri'), 'https://facebook.com/profile.php?id=dimitri')
        self.assertIsNone(utils.clean_facebook('N/A'))
        self.assertIsNone(utils.clean_facebook('NA'))
        self.assertIsNone(utils.clean_facebook('na'))
        self.assertIsNone(utils.clean_facebook(''))

    def test_clean_instagram(self):
        expected = 'https://instagram.com/claude'
        self.assertEqual(utils.clean_instagram('https://www.instagram.com/claude'), expected)
        self.assertEqual(utils.clean_instagram('Www.instagram.com/claude'), expected)
        self.assertEqual(utils.clean_instagram('https://instagram.com/claude'), expected)
        self.assertEqual(utils.clean_instagram('instagram.com/claude'), expected)
        self.assertEqual(utils.clean_instagram('Instagram.com/claude'), expected)
        self.assertEqual(utils.clean_instagram('@claude'), expected)
        self.assertEqual(utils.clean_instagram('claude'), expected)
        self.assertIsNone(utils.clean_instagram('N/A'))
        self.assertIsNone(utils.clean_instagram('NA'))
        self.assertIsNone(utils.clean_instagram('na'))
        self.assertIsNone(utils.clean_instagram(''))

    def test_clean_twitter(self):
        expected = 'https://twitter.com/edelgard'
        self.assertEqual(utils.clean_twitter('https://www.twitter.com/edelgard'), expected)
        self.assertEqual(utils.clean_twitter('Www.twitter.com/edelgard'), expected)
        self.assertEqual(utils.clean_twitter('https://twitter.com/edelgard'), expected)
        self.assertEqual(utils.clean_twitter('twitter.com/edelgard'), expected)
        self.assertEqual(utils.clean_twitter('Twitter.com/edelgard'), expected)
        self.assertEqual(utils.clean_twitter('https://mobile.twitter.com/edelgard'), expected)
        self.assertEqual(utils.clean_twitter('@edelgard'), expected)
        self.assertEqual(utils.clean_twitter('edelgard'), expected)
        self.assertIsNone(utils.clean_twitter('N/A'))
        self.assertIsNone(utils.clean_twitter('NA'))
        self.assertIsNone(utils.clean_twitter('na'))
        self.assertIsNone(utils.clean_twitter(''))

    def test_convert_camelcase_to_slugified(self):
        camel = "ACamelCaseString"
        slugified = utils.convert_camelcase_to_slugified(camel)
        self.assertEqual(slugified, "a-camel-case-string")

    def test_convert_camelcase_to_slugified_already_slugified(self):
        camel = "a-camel-case-string"
        slugified = utils.convert_camelcase_to_slugified(camel)
        self.assertEqual(slugified, "a-camel-case-string")
