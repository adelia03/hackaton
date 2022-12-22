from django.test import TestCase

from main.logic import operations

class LogicTestCase(TestCase):
    def test_plus(self):
        result = operations(9, 8, '+')
        self.assertEqual(17, result)