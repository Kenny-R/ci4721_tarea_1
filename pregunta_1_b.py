'''
Ejemplo de parseo de JSON basado en el ejemplo de la libreria parsec.py 

https://github.com/sighingnow/parsec.py/blob/master/examples/jsonc.py
'''

import re
from parsec import *

# eliminamos los espacios en blanco
white_space = regex(r'\s*', re.MULTILINE)
def lexme(p): return p << white_space


# definimos los simbolos terminales
open_bracket = lexme(string('['))
close_bracket = lexme(string(']'))
open_brace = lexme(string('{'))
close_brace = lexme(string('}'))
colon = lexme(string(':'))
comma = lexme(string(','))

true = lexme(string('true')).result(True)
false = lexme(string('false')).result(False)
null = lexme(string('null')).result(None)


def number():
    '''
    Parsea un numero, este puede ser enteros o flotantes
    '''
    return lexme(regex(r'-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?')).parsecmap(float)


def char_seq():
    '''
    Parsea un Cadena de caracteres con caracteres normales y caracteres escapados
    '''

    def normal_char():
        '''
        Una cadena de caracteres normales sin comillas ni barras
        '''
        return regex(r'[^"\\]+')

    def escp_char():
        '''
        Caracteres escapados dentro de una cadena de caracteres
        '''
        
        return string('\\') >> (
                string('"') 
                | string('\\') 
                | string('/') 
                | string('b').result('\b') 
                | string('f') .result('\f')
                | string('n').result('\n')  
                | string('r').result('\r')
                | string('t').result('\t')
                | regex(r'u[0-9a-fA-F]{4}')).parsecmap(lambda x: chr(int(x[1:], 16)))
    
    return normal_char() | escp_char()


# definimos las reglas
@lexme
@generate
def quoted():
    '''
    Parsea una cadena de caracteres entre comillas
    '''
    yield string('"')
    result = yield many(char_seq())
    yield string('"')
    return ''.join(result)

@generate
def json_object():
    '''
    Parsea  un objeto JSON 
    '''
    yield open_brace
    l = yield optional(object_list, None)
    yield close_brace
    
    if l is None:
        return []
    
    return l


@generate
def object_list():
    '''
    Parsea una lista de objetos que van contenidos en un objeto JSON
    '''
    s = yield quoted
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
    Funcion auxiliar para parsear una lista de objetos contenidos en un objeto JSON
    '''
    yield comma
    s = yield quoted
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
    Parsea los valores que pueden ir a la derecha de un par clave-valor en un objeto JSON
    '''
    v = yield quoted | number() | json_object | array_json
    return v


@generate
def array_json():
    '''
    Parsea un arreglo vacio y con contenido
    '''
    yield open_bracket
    x = yield optional(array_list, None)
    yield close_bracket

    if x is None:
        return []

    return x


@generate
def array_list():
    '''
    Parsea una lista de valores que van dentro de un arreglo JSON
    '''
    v = yield value
    result = [v]

    # Si Y es lambda, entonces no se hace nada
    y = yield optional(array_list_tail, None)
    if y:
        result += y
    return result


@generate
def array_list_tail():
    '''
    Funcion auxiliar para parsear una lista de valores que van dentro de un arreglo JSON
    '''
    yield comma
    v = yield value
    result = [v]
    y = yield optional(array_list_tail, None)
    if y:
        result += y
    return result


# Los valores posibles de un JSON
value = quoted | number() | json_object | array_json | true | false | null

# El parser de json

json = white_space >> json_object

if __name__ == '__main__':
    input_str = input("Introduce la frase en JSON que quiere parsear: ")
    try:
        result = json_object.parse(input_str)
        print("Fino, se parseo bien la frase, el resultado es: ", result)
    except Exception as e:
        print(
            f"No se pudo parsear correctamente la frase dio el error: \n{e}.")
