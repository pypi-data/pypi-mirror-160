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
        self.assertEqual(PyDash.title("hello world"), "Hello World")
        self.assertNotEqual(PyDash.title("hELLO wORLD"), "hello world")

    def test_kebab_method(self):
        self.assertEqual(PyDash.kebab("Kebab case adds hyphens BetWEEN lowerCASE text"),
                         "kebab-case-adds-hyphens-between-lowercase-text")
        self.assertNotEqual(PyDash.kebab("Kebab case doesn't contain spaces"), "kebab-case-doesn't contain spaces")

# testpypi token :
# pypi-AgENdGVzdC5weXBpLm9yZwIkYjA4ZjFhODYtOWI3MC00MDdmLTk3ZTMtMTJjNjUzMjlkNTJiAAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiBf2BkdQN3JuoQncHr1u__OvUQJBxaPG8kWK84Uzr-gkA        

# Using this token
# To use this API token:

# Set your username to __token__
# Set your password to the token value, including the pypi- prefix
# For example, if you are using Twine to upload your projects to PyPI, set up your $HOME/.pypirc file like this:

# [testpypi]
#   username = __token__
#   password = pypi-AgENdGVzdC5weXBpLm9yZwIkYjA4ZjFhODYtOWI3MC00MDdmLTk3ZTMtMTJjNjUzMjlkNTJiAAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiBf2BkdQN3JuoQncHr1u__OvUQJBxaPG8kWK84Uzr-gkA


## TOKEN di  pypi (bukan test.pipy)
# pypi-AgEIcHlwaS5vcmcCJDkwY2YxODQwLWNmNDktNGMwNi1iMTI4LWUxZDkyODA5MjFlNgACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgCUKN8sIE-Wakx3Hq7hCB96kFXi6nNwZL2NgUjOBjRZo