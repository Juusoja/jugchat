import sys
import unittest

class Testy(unittest.TestCase):

    ch1 = "asdfghjk"
    ch2 = "ashjk"

    def test_string(self):
	ch1 = "asdfghjk"
	ch2 = "ashjk"

	self.assertEqual(ch1, ch2)


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
