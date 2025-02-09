'''
Ejemplo de parseo de JSON basado en el ejemplo de la libreria parsec.py 

https://github.com/sighingnow/parsec.py/blob/master/examples/jsonc.py

El lenguaje que queremos parsear es el siguiente:
    S -> J
    J -> {L}
    L -> s:VR
    R -> ,s:VR | lambda
    V -> s | n | J | A
    A -> [X]
    X -> VY
    Y -> ,VY | lambda
con los simbolos terminales: s, n, [, ], {, }, :, ,
'''

import re
from parsec import * 

# eliminamos los espacios en blanco
white_space = regex(r'\s*', re.MULTILINE)
lexme = lambda p: p << white_space

# definimos los simbolos terminales
s_token = lexme(string('s'))
n_token = lexme(string('n'))
open_bracket = lexme(string('['))
close_bracket = lexme(string(']'))
open_brace = lexme(string('{'))
close_brace = lexme(string('}'))
colon = lexme(string(':'))
comma = lexme(string(','))

# definimos las reglas

@generate
def object_json():
    '''
    J -> {L}
    '''
    yield open_brace
    l = yield sepBy(object_list, comma)
    yield close_brace
    return l

@generate
def object_list():
    '''
    L -> s:VR
    '''
    s = yield s_token
    yield colon
    v = yield value
    return (s, v)

@generate
def array():
    '''
    A -> [X]
    '''
    yield open_bracket
    x = yield array_items
    yield close_bracket
    return x

@generate
def array_items():
    '''
    X -> VY
    '''
    v = yield sepBy(value, comma)
    return v

# V -> s | n | J | A
value = s_token | n_token | object_json | array

if __name__ == '__main__':
    json_str = '{s:n, s:s, s:{s:n, s:n}, s:[n, s, {s:n, s:s}]}'
    print(object_json.parse(json_str))