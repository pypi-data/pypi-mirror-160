from itertools import chain


class Tabulator:

    def __init__(self, docs, name, foreign_keys):
        self._docs = docs
        self.name = name
        self.primary_key = f"{self.name}.__id__"
        self.foreign_keys = foreign_keys
        self.all_keys = [self.primary_key] + self.foreign_keys
        self._insert_index()

    def tabulate(self):
        if self._check_no_dicts():
            more_docs = [(k, self._extract_list_field(k), self.all_keys) for k in self._get_list_fields()]
            fields = list(dict.fromkeys(chain.from_iterable(d.keys() for d in self._docs)).keys())
            data = {k: [d.get(k) for d in self._docs] for k in fields}
            return data, more_docs
        else:
            self._flatten_one_level()
            return self.tabulate()

    def _insert_index(self):
        for i in range(len(self._docs)):
            self._docs.append({self.primary_key: i, **self._docs.pop(0)})

    def _check_no_dicts(self):
        return all(type(v) is not dict for d in self._docs for v in d.values())

    def _get_list_fields(self):
        return sorted(set(k for d in self._docs for k, v in d.items() if type(v) is list))

    def _extract_list_field(self, k):
        docs = []
        for d in self._docs:
            if k in d.keys():
                v = d.pop(k)
                id_d = {x: y for x, y in d.items() if x in self.all_keys}
                for v_ in v:
                    docs.append({**id_d, k: v_})
        return docs

    def _flatten_one_level(self):
        for d in self._docs:
            for k in list(d.keys()):
                v = d[k]
                if type(v) is dict:
                    for k_, v_ in v.items():
                        d[f"{k}.{k_}"] = v_
                    del d[k]
