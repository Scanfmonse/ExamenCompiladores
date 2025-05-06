import re
import os

keywords = set()
delimit = set()
operador = set()
contenedor = set()
constantes = []
conteo_variables = {}

def analizar_codigo(content):
    cpp_keywords = {
        'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
        'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
        'inline', 'int', 'long', 'register', 'restrict', 'return', 'short',
        'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
        'unsigned', 'void', 'volatile', 'while',
        'bool', 'class', 'const_cast', 'delete', 'dynamic_cast', 'explicit',
        'export', 'false', 'friend', 'mutable', 'namespace', 'new', 'operator',
        'private', 'protected', 'public', 'reinterpret_cast', 'static_cast',
        'template', 'this', 'throw', 'true', 'try', 'typeid', 'typename',
        'using', 'virtual', 'wchar_t', 'cout', 'cin', 'endl', 'return','stdio','printf','scanf'        
        
    }

    cpp_end = {';', ','}
    cpp_operador = ['++', '--', '<<', '!=', '&&', '+=', '-=', '>=', '<=', '+', '*', '%','<', '>', '#', ':', '==', '=']
    cpp_contenedores = {'(', ')', '{', '}'}
    tipos_dato = ['int', 'float', 'double', 'char', 'bool', 'string']
    patron_variables = r'\b(?:' + '|'.join(tipos_dato) + r')\s+([a-zA-Z_]\w*)'

    content = re.sub(r'//.*|/\*[\s\S]*?\*/', '', content)  # Elimina comentarios
    pattern_operators = '|'.join(re.escape(op) for op in sorted(cpp_operador, key=lambda x: -len(x)))
    # Limpieza de comentarios
    content = re.sub(r'//.*|/\*[\s\S]*?\*/', '', content)

    # Inicializar contadores y conjuntos
    countRes = countDel = countOpe = countCont = countConst = 0

    # Palabras y operadores
    words = re.findall(r'\b\w+\b|[;,.]', content)
    pattern_operators = '|'.join(re.escape(op) for op in sorted(cpp_operador, key=lambda x: -len(x)))
    found_operators = re.findall(pattern_operators, content)

    for op in found_operators:
        operador.add(op)
        countOpe += 1

    # Constantes numéricas
    for match in re.finditer(r'\b\d+(\.\d+)?\b', content):
        constantes.append(match.group())
        countConst += 1

    for word in words:
        if word in cpp_keywords:
            keywords.add(word)
            countRes += 1

    for char in content:
        if char in cpp_end:
            delimit.add(char)
            countDel += 1
        if char in cpp_contenedores:
            contenedor.add(char)
            countCont += 1

    # Variables
    nombres_variables = re.findall(patron_variables, content)
    variables = {var for var in nombres_variables if var not in cpp_keywords}
    for var in variables:
        apariciones = len(re.findall(r'\b' + re.escape(var) + r'\b', content))
        conteo_variables[var] = apariciones

    # Constantes de cadenas
    cadenas = []
    en_cadena = False
    cadenaEncontrada = ''
    for c in content:
        if c == '"':
            if en_cadena:
                cadenas.append(f'"{cadenaEncontrada}"')
                cadenaEncontrada = ''
                en_cadena = False
            else:
                en_cadena = True
        elif en_cadena:
            cadenaEncontrada += c
    constantes.extend(cadenas)
    countConst += len(cadenas)

    # Crear salida de texto
    resultado = []
    resultado.append(f"Número de palabras reservadas: {countRes}")
    resultado.append(f"Número de delimitadores en el código: {countDel}")
    resultado.append(f"Número de operadores en el código: {countOpe}")
    resultado.append(f"Número de contenedores en el código: {countCont // 2}")
    resultado.append(f"Constantes encontradas en el código: {countConst}")
    for i, c in enumerate(constantes, 1):
        resultado.append(f"{i}: {c}")
    resultado.append(f"Total de usos de variables en el código: {sum(conteo_variables.values())}")
    for nombre, conteo in conteo_variables.items():
        resultado.append(f"{nombre}: {conteo}")

    return "\n".join(resultado)

