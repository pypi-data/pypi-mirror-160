# This file is placed in the Public Domain.


"model tests"


import unittest


from genocide.model import oorzaak
from genocide.object import Object


class Test_Composite(unittest.TestCase):

    def test_composite(self):
        self.assertEqual(type(oorzaak), Object)
