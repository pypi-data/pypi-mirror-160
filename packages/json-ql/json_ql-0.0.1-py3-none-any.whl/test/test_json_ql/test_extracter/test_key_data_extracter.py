from typing import Any
import pytest

from json_ql.extracter.key_data_extracter import KeyDataExtracter


class TestKeyDataExtracter:

    @pytest.mark.parametrize('object,key,output', [
        # happy path with key
        ({"name": "myname"}, "name", "myname"),
        # key doesn't exist
        ({"name": "myname"}, "age", None),
        # key from list
        ([{"name": "myname"}, {"name": "myname2"}], "name", ["myname", "myname2"]),
        # key from list some matching
        ([{"name": "myname"}, {"age": "2222"}], "name", ["myname", None]),
    ])
    def test_extract(self, object: Any, key: str, output: Any):
        assert KeyDataExtracter().extract(object, key) == output
