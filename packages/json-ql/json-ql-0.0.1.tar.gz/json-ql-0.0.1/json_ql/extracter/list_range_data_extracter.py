from .data_extracter import DataExtracter


class ListRangeDataExtracter(DataExtracter):
    def __init__(self):
        super().__init__()

    def extract(self, lst: list, key: tuple):
        try:
            start_index, end_index = map(int, key)
            for i in range(start_index, end_index):
                return lst[start_index:end_index]
            return None
        except Exception:
            return None
