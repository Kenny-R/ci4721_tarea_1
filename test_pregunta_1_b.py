import pytest
from pregunta_1_b import object_json


def test_simple_object():
    json_str = '{s:n}'
    result = object_json.parse(json_str)
    assert result == [('s', 'n')]


def test_nested_object():
    json_str = '{s:{s:n}}'
    result = object_json.parse(json_str)
    assert result == [('s', [('s', 'n')])]


def test_array_in_object():
    json_str = '{s:[n, s]}'
    result = object_json.parse(json_str)
    assert result == [('s', ['n', 's'])]


def test_complex_object():
    json_str = '{s:n, s:s, s:{s:n}, s:[n, s]}'
    result = object_json.parse(json_str)
    assert result == [('s', 'n'), ('s', 's'),
                      ('s', [('s', 'n')]), ('s', ['n', 's'])]


if __name__ == '__main__':
    pytest.main()
