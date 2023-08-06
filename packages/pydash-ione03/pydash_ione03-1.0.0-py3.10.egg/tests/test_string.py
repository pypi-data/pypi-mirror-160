import unittest

from pydash import PyDash

class Test(unittest.TestCase):
    def test_lower_method(self):
        self.assertEqual(PyDash.lower("TEST"), "test")
        self.assertNotEqual(PyDash.lower("test"), "TEST")

    def test_upper_method(self):
        self.assertEqual(PyDash.upper("test"), "TEST")
        self.assertNotEqual(PyDash.upper("TEST"), "test")

    def test_title_method(self):
        self.assertEqual(PyDash.title("hello world"), "Hello world")
        self.assertNotEqual(PyDash.title("hELLO wORLD"), "hello world")

    def test_kebab_method(self):
        self.assertEqual(PyDash.kebab("Kebab case adds hyphens BetWEEN lowerCASE text"),
                         "kebab-case-adds-hyphens-between-lowercase-text")
        self.assertNotEqual(PyDash.kebab("Kebab case doesn't contain spaces"), "kebab-case-doesn't contain spaces")