class Table:

    def __init__(self, data, primary_key, foreign_keys):
        self.data = data
        self.primary_key = primary_key
        self.foreign_keys = foreign_keys
        self.all_keys = [self.primary_key] + self.foreign_keys
        self.columns = list(self.data.keys())
        self.n_rows = len(data[list(data.keys())[0]])

    def rename(self, name):
        old_pk = self.primary_key
        self.primary_key = f"{name}.__id__"
        self.all_keys = [self.primary_key] + self.foreign_keys
        self.data = {(self.primary_key if k == old_pk else k): v for k, v in self.data.items()}
        self.columns = list(self.data.keys())

    def rename_fk(self, current_fk, new_fk):
        for i in range(len(self.foreign_keys)):
            if self.foreign_keys[i] == current_fk:
                self.foreign_keys[i] = new_fk
        self.all_keys = [self.primary_key] + self.foreign_keys
        self.data = {(new_fk if k == current_fk else k): v for k, v in self.data.items()}
        self.columns = list(self.data.keys())

    def rename_column(self, current_name, new_name):
        self.data = {(new_name if k == current_name else k): v for k, v in self.data.items()}
        self.columns = list(self.data.keys())

    def merge_columns(self, col1, col2):
        self.data[col1] = [v2 if v1 is None else v1 for v1, v2 in zip(self.data[col1], self.data[col2])]
        del self.data[col2]
        self.columns = list(self.data.keys())

    def generate_metadata(self):
        metadata = []
        for c in self.columns:
            values = self.data[c]
            nullable = any(v is None for v in values)
            non_null_values = [v for v in values if v is not None]
            data_type = self._determine_type(non_null_values)
            unique = len(non_null_values) == len(set(non_null_values))
            metadata.append({"column": c, "type": data_type, "nullable": nullable, "unique": unique})
        return metadata

    @staticmethod
    def _determine_type(values):
        if len(values) == 0:
            return "any"
        elif all(type(v) is bool for v in values):
            return "boolean"
        elif all(type(v) in [int, float] for v in values):
            return "number"
        elif all(type(v) is str for v in values):
            return "string"
        else:
            return "any"
