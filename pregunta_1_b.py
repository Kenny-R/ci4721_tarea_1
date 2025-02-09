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
import sys

# eliminamos los espacios en blanco
white_space = regex(r'\s*', re.MULTILINE)
def lexme(p): return p << white_space


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
    l = yield object_list
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
    result = [(s, v)]
    
    # Si R es lambda, entonces no se hace nada
    r = yield optional(object_list_tail, None)
    if r:
        result += r
    return result


@generate
def object_list_tail():
    '''
    R -> ,s:VR | lambda
    '''
    yield comma
    s = yield s_token
    yield colon
    v = yield value
    result = [(s, v)]
    
    # Si R es lambda, entonces no se hace nada
    r = yield optional(object_list_tail, None)
    if r:
        result += r
    
    return result


@generate
def value():
    '''
    V -> s | n | J | A
    '''
    v = yield s_token | n_token | object_json | array_json
    return v


@generate
def array_json():
    '''
    A -> [X]
    '''
    yield open_bracket
    x = yield array_list
    yield close_bracket
    return x


@generate
def array_list():
    '''
    X -> VY
    '''
    v = yield value
    result = [v]
    
    # Si Y es lambda, entonces no se hace nada
    y= yield optional(array_list_tail, None)
    if y:
        result += y
    return result


@generate
def array_list_tail():
    '''
    Y -> ,VY | lambda
    '''
    yield comma
    v = yield value
    result = [v]
    y= yield optional(array_list_tail, None)
    if y:
        result += y
    return result


# V -> s | n | J | A
value = s_token | n_token | object_json | array_json

if __name__ == '__main__':
    input_str = input("Introduce la frase en JSON que quiere parsear: ")
    try:
        result = object_json.parse(input_str)
        print("Fino, se parseo bien la frase, el resultado es: ", result)
    except Exception as e:
        print(f"No se pudo parsear correctamente la frase dio el error: \n{e}.")
