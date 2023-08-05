from relatable.tabulator import Tabulator
from relatable.table import Table

from copy import copy, deepcopy


class RelationalSchema:

    def __init__(self, docs, main_entity_name="main"):
        self.tables = {}
        self._docs_list = [(main_entity_name, docs, [])]
        self._make()

    def to_list(self):
        return [t.data for t in self.tables.values()]

    def rename_table(self, current_name, new_name):
        current_fk = f"{current_name}.__id__"
        new_fk = f"{new_name}.__id__"
        for k, t in self.tables.items():
            if k == current_name:
                t.rename(new_name)
            elif current_fk in t.foreign_keys:
                t.rename_fk(current_fk, new_fk)
        self.tables = {(new_name if k == current_name else k): t for k, t in self.tables.items()}

    def generate_metadata(self):
        return [{"table": k, **d} for k, t in self.tables.items() for d in t.generate_metadata()]

    def _make(self):
        i = 0
        while len(self._docs_list) > 0:
            name, docs, foreign_keys = self._docs_list.pop()
            tab = Tabulator(deepcopy(docs), name, copy(foreign_keys))
            data, more_docs = tab.tabulate()
            new_table = Table(data, tab.primary_key, tab.foreign_keys)
            self.tables[name] = new_table
            self._docs_list.extend(more_docs)
            i += 1
