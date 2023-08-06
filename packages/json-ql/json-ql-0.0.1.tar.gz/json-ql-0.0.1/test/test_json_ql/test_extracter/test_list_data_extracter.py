from typing import Any, List
import pytest

from json_ql.extracter.list_data_extracter import ListDataExtracter


class TestListDataExtracter:

    @pytest.mark.parametrize('lst,index,output', [
        # happy path with key
        (["a", "b"], 0, "a"),
        # key doesn't exist
        (["a", "b"], 3, None),
    ])
    def test_extract(self, lst: List, index: int, output: Any):
        assert ListDataExtracter().extract(lst, index) == output
