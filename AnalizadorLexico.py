import re
keywords = set()
delimit = set()
operador = set()
contenedor = set()
constantes = []
conteo_variables = {}

def analizar_codigo(content):
    cpp_keywords = {
        'int', 'float', 'double', 'char', 'if', 'else', 'for', 'while', 'do', 'switch',
        'case', 'default', 'return', 'break', 'continue', 'class', 'struct', 'public',
        'private', 'protected', 'void', 'static', 'const', 'new', 'delete', 'try',
        'catch', 'throw', 'namespace', 'using', 'include', 'define', 'template', 'cout',
        'endl', 'string', 'bool', 'iostream', 'std', 'main', 'true', 'false'
    }
    cpp_end = {';', ','}
    cpp_operador = ['++', '--', '<<', '!=', '&&', '+=', '-=', '>=', '<=', '+', '*', '%','<', '>', '#', ':', '==', '=']
    cpp_contenedores = {'(', ')', '{', '}'}
    tipos_dato = ['int', 'float', 'double', 'char', 'bool', 'string']
    patron_variables = r'\b(?:' + '|'.join(tipos_dato) + r')\s+([a-zA-Z_]\w*)'

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

"""
Codigo anterior por si las dudas :)

import re #importamos el que ayuda a reconocer expresiones regulares

# Lista de palabras reservadas en C++
cpp_keywords = {
    'int', 'float', 'double', 'char', 'if', 'else', 'for', 'while', 'do', 'switch',
    'case', 'default', 'return', 'break', 'continue', 'class', 'struct', 'public',
    'private', 'protected', 'void', 'static', 'const', 'new', 'delete', 'try',
    'catch', 'throw', 'namespace', 'using', 'include', 'define', 'template','cout',
    'endl','string', 'bool', 'using', 'iostream' ,'std', 'main','true','false'
}
#Comentario
cpp_end = {
    ';',','
}

cpp_operador = [
    '++', '--', '<<', '!=', '&&', '+=', '-=', '>=', '<=', '+', '*', '<', '>', '#',':','=='
]

cpp_contenedores = {
    '(',')','{','}'
}

tipos_dato = ['int', 'float', 'double', 'char', 'bool', 'string']
patron_variables = r'\b(?:' + '|'.join(tipos_dato) + r')\s+([a-zA-Z_]\w*)'

# Clasificaciones
keywords = set()
countRes = 0

delimit = set ()
countDel = 0

operador = set ()
countOpe = 0 

contenedor = set ()
countCont = 0

constantes = []  # Constantes numéricas y cadenas unificadas
countConst = 0

countVar = 0


with open('archivo.cpp', 'r') as f:
    content = f.read()
    content = re.sub(r'//.*|/\*[\s\S]*?\*/', '', content)
    # Extrae las palabras
    words = re.findall(r'\b\w+\b|[;,.]', content) 


    pattern_operators = '|'.join(re.escape(op) for op in sorted(cpp_operador, key=lambda x: -len(x)))

    # Buscamos todos los operadores en el contenido
    found_operators = re.findall(pattern_operators, content)

    for op in found_operators:
        operador.add(op)
        countOpe += 1
    
    # Buscar constantes numéricas (enteros y decimales)
    numeros = re.findall(r'\b\d+(\.\d+)?\b', content)
    for match in re.finditer(r'\b\d+(\.\d+)?\b', content):
        constantes.append(match.group())
        countConst += 1

    for word in words:
        if word in cpp_keywords:
            keywords.add(word)
            countRes+=1
    
    for word in content:
        if word in cpp_keywords:
            keywords.add(word)
            countRes+=1
        if word in cpp_end :
            delimit.add(word)
            countDel+=1
        if word in cpp_contenedores :
            contenedor.add(word)
            countCont+=1
    
nombres_variables = re.findall(patron_variables, content)
variables = {var for var in nombres_variables if var not in cpp_keywords}

conteo_variables = {}
for var in variables:
    apariciones = len(re.findall(r'\b' + re.escape(var) + r'\b', content))
    conteo_variables[var] = apariciones
        
def charArchiv(nombre_archivo):   #Obtenemos todos los chars del archivo
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
        chars = list(contenido)  #Convierte el contenido en una lista de chars
        return chars

# Función para detectar cadenas entre comillas
def constantesCadenas(chars):
    cadenas = []
    en_cadena = False
    cadenaEncontrada = ''

    for c in chars:
        if c == '"':
            if en_cadena:
                cadenas.append(f'"{cadenaEncontrada}"')  # Agregar las comillas
                cadenaEncontrada = ''
                en_cadena = False
            else:
                en_cadena = True
        elif en_cadena:
            cadenaEncontrada += c
    return cadenas

chars = charArchiv('archivo.cpp')  # Pasa el nombre del archivo como parámetro

def charArchiv(chars):  
    with open(chars, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
        return list(contenido)



cadenas = constantesCadenas(chars)
constantes.extend(cadenas)
countConst += len(cadenas)

# --- Resultados ---
# print("Número de palabras reservadas:", keywords)
print("Número de palabras reservadas:", countRes)
print("Número de delimitadores en el código:", countDel)
print("Número de operadores en el código:", countOpe)
print("Número de contenedores en el código:", countCont/2)
print("Constantes encontradas en el código:", countConst)
for i, c in enumerate(constantes, 1):
    print(f'{i}: {c}')
print("Total de usos de variables en el código:", sum(conteo_variables.values()))
for nombre, conteo in conteo_variables.items():
    print(f'{nombre}: {conteo}')"""
