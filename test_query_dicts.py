import unittest
from query_dicts import *

class TestQueryDicts(unittest.TestCase):

    def setUp(self):
        self.ds = [{"a": 1, "b": 2}, {"b": 22, "c": 3}]
        self.qd = QueryDicts(self.ds)

    def tearDown(self):
        del self.ds
        del self.qd

    def test_set_keys(self):
        self.assertEqual(self.qd.keys, {"a", "b", "c"})

    def test_add_dict(self):
        self.qd.add_dict({"c": 33, "d": 4})
        self.assertEqual(self.qd.keys, {"a", "b", "c", "d"})
        self.assertEqual(len(self.qd.ds), 3)

    def test_eval_filter_str(self):
        self.assertTrue(self.qd.eval_filter_str("a > 0", {"a": 1, "b": 2}))
        self.assertTrue(self.qd.eval_filter_str("a < b", {"a": 1, "b": 2}))
        self.assertTrue(self.qd.eval_filter_str("-1.5 < b", {"a": 1, "b": 2}))
        self.assertTrue(self.qd.eval_filter_str("a != b", {"a": 1, "b": 2}))
        self.assertTrue(self.qd.eval_filter_str("a in b", {"a": 1, "b": [1]}))
        self.assertTrue(self.qd.eval_filter_str("a != b", {"a": 1, "b": 2}))
        self.assertTrue(self.qd.eval_filter_str("not a", {"a": False, "b": 2}))
        self.assertTrue(self.qd.eval_filter_str("a is not b", {"a": 1, "b": 2}))
        self.assertTrue(self.qd.eval_filter_str("a is b", {"a": 1.5, "b": 1.5}))
        self.assertTrue(self.qd.eval_filter_str("True", {"z": None}))

    def test_select(self):
        self.qd.select("a", "b", "c")
        self.assertEqual(self.qd.result_fields, ("a", "b", "c"))

    def test_where(self):
        self.qd.select("a", "b")
        self.assertEqual(self.qd.where("a == 1"), [{"a": 1, "b": 2}])

    def test_query_dicts(self):
        res1 = query_dicts(self.ds).select("a", "c").where("b != 7")
        exp1 = [{"a": 1, "c": None}, {"a": None, "c": 3}]
        self.assertEqual(res1, exp1)

        res2 = QueryDicts(exp1).select("c", "d").where("a")
        exp2 = [{"c": None, "d": None}]
        self.assertEqual(res2, exp2)
