""" Query a list of dictionaries with a SQL-like interface.

Instance methods are named and implemented to enable a left-to-right SQL syntax.

Example:
    d_list = [
        {"id": 1, "name": "Leo", "height": 1.9, "retired": True},
        {"id": 2, "name": "Szymon", "height": 1.72, "retired": False},
        {"id": 3, "name": "Giorgi", "height": 1.77, "retired": False},
        # ...
    ]

    query_dicts(d_list).select("id", "name").where("retired")
    > [{"id": 1, "name": "Leo"}]

    query_dicts(d_list).select("id").where("height > 1.75")
    > [{"id": 1}, {"id": 3}]

    query_dicts(d_list).select("name", "height").where({"id": lambda x: x%2 == 0})
    > [{"name": "Szymon", "height": 1.72}]
"""
from functools import reduce
from operators import OPS, run_op
from re import finditer, match


_PATTERNS = ["(?P<op>{})".format("|".join(OPS))]
_PATTERNS += ["(?P<skip>\s+)"]
_PATTERNS += ["(?P<float>-?\d?\.\d+)"]
_PATTERNS += ["(?P<int>-?\d+\.?)"]
_PATTERNS += ["(?P<bool>[Tt]rue|[Ff]alse)"]

class QueryDicts:
    def __init__(self, dicts=None, result_fields=None):
        self.dicts = dicts or []
        self.result_fields = result_fields
        self.result = []
        self.keys = reduce(lambda x, y: x.union(y), self.dicts, set())

    def get_patterns(self):
        return _PATTERNS + ["(?P<field>{})".format("|".join(self.keys))]

    def add_dicts(self, ds):
        self.dicts += ds
        self.keys = reduce(lambda x, y: x.union(y), self.dicts, set())

    def add_dict(self, d):
        self.dicts.append(d)
        self.keys |= set(d)

    def select(self, *fields):
        self.result_fields = fields
        return self

    def where(self, *filters):
        res = self.dicts.copy()

        for f in filters:
            if type(f) == dict:
                for field, func in f.items():
                    res = [d for d in res if d.get(field) and func(d[field])]
            elif type(f) == str:
                res = [d for d in res if self.eval_filter_str(f, d)]

        return [dict([(f, d.get(f)) for f in self.result_fields]) for d in res]

    def parse_filter_str(self, s):
        for mo in finditer("|".join(self.get_patterns()), s):
            kind = mo.lastgroup
            value = mo.group(kind)
            yield (kind, value)

    def eval_filter_str(self, f, d):
        e = Exception("Bad filter: {}".format(f))
        v1 = v2 = op = None

        for (kind, value) in self.parse_filter_str(f):
            if kind == "op":
                if op is not None: raise e
                op = value

            elif kind != "skip":
                if kind == "field": value = d.get(value)
                if kind == "float": value = float(value)
                if kind == "int": value = int(value)
                if kind == "bool": value = bool(value)

                if v1 is None: v1 = value
                elif v2 is None: v2 = value
                else: raise e

        return run_op(op, v1, v2)


class FromDicts(QueryDicts):
    def from_dicts(self, ds):
        if self.dicts and match("[Nn].*", input("Overwrite dicts (y/n)? ")):
            return "Aborting..."

        self.add_dicts(ds)
        return self


def query_dicts(ds): return QueryDicts(dicts=ds)


def select_fields(*fields): return FromDicts(result_fields=fields)
