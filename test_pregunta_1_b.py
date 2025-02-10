import pytest
from pregunta_1_b import json


def test_simple_objects():
    result = json.parse('{"s":"hola mundo"}')
    assert result == [("s", "hola mundo")]
    
    result = json.parse('{"entero": 10}')
    assert result == [("entero", 10)]
    
    result = json.parse('{"flotante": 3.1416}')
    assert result == [("flotante", 3.1416)]
    
    result = json.parse('{"Velda": true}')
    assert result == [('Velda', True)]
    
    result = json.parse('{"Falso": false}')
    assert result == [('Falso', False)]
    
    result = json.parse('{"Nothing": null}')
    assert result == [('Nothing', None)]

def test_nested_object():
    result = json.parse('{"primer nivel":{"segundo nivel": "fin"}}')
    assert result == [('primer nivel', [('segundo nivel', 'fin')])]

def test_array_in_object():
    result = json.parse('{"Arreglo":["item", 10, 3.14]}')
    assert result == [('Arreglo', ['item', 10, 3.14])]

def test_empty_object():
    result = json.parse('{}')
    assert result == []

def test_empty_array():
    result = json.parse('{"arreglo vacio": []}')
    assert result == [("arreglo vacio", [])]


def test_complex_object():
    result = json.parse('{"s_1":3.1416, "s_2":"s_2_1", "s_3":{"s_3_1":10}, "s_4":[25, "s_4_1"]}')
    assert result == [('s_1', 3.1416), ('s_2', 's_2_1'), ('s_3', [('s_3_1', 10.0)]), ('s_4', [25.0, 's_4_1'])]

if __name__ == '__main__':
    pytest.main()
