import unittest

from preserves import *
from preserves.path import parse

class BasicPathTests(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(parse('').exec(1), (1,))
        self.assertEqual(parse('').exec([]), ([],))
        self.assertEqual(parse('').exec(Record(Symbol('hi'), [])), (Record(Symbol('hi'), []),))

    def test_children(self):
        self.assertEqual(parse('/').exec([1, 2, 3]), (1, 2, 3))
        self.assertEqual(parse('/').exec([1, [2], 3]), (1, [2], 3))
        self.assertEqual(parse('/').exec(Record(Symbol('hi'), [1, [2], 3])), (1, [2], 3))

    def test_label(self):
        self.assertEqual(parse('.^').exec([1, 2, 3]), ())
        self.assertEqual(parse('.^').exec([1, [2], 3]), ())
        self.assertEqual(parse('.^').exec(Record(Symbol('hi'), [1, [2], 3])), (Symbol('hi'),))

    def test_count(self):
        self.assertEqual(parse('<count / ^ hi>').exec([ Record(Symbol('hi'), [1]),
                                                        Record(Symbol('no'), [2]),
                                                        Record(Symbol('hi'), [3]) ]),
                         (2,))
        self.assertEqual(parse('/ <count ^ hi>').exec([ Record(Symbol('hi'), [1]),
                                                        Record(Symbol('no'), [2]),
                                                        Record(Symbol('hi'), [3]) ]),
                         (1, 0, 1))
