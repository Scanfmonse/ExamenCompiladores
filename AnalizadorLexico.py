import re #importamos el que ayuda a reconocer expresiones regulares

# Lista de palabras reservadas en C++
cpp_keywords = {
    'int', 'float', 'double', 'char', 'if', 'else', 'for', 'while', 'do', 'switch',
    'case', 'default', 'return', 'break', 'continue', 'class', 'struct', 'public',
    'private', 'protected', 'void', 'static', 'const', 'new', 'delete', 'try',
    'catch', 'throw', 'namespace', 'using', 'include', 'define', 'template','cout',
    'endl','string', 'bool', 'using', 'iostream' ,'std', 'main'
}
#Comentario
cpp_end = {
    ';','.',','
}

cpp_operador = [
    '++', '--', '<<', '!=', '&&', '+=', '-=', '>=', '<=', '=', '+', '*', '<', '>', '#'
]

cpp_contenedores = {
    '(',')','{','}'
}

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
        
def charArchiv(nombre_archivo):   #Obtenemos todos los chars del archivo
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
        chars = list(contenido)  #Convierte el contenido en una lista de chars
        return chars

#chars = charArchiv('archivo.cpp')
#print(chars)  #Muestra todos los chars del archivo
#print("Total de chars:", len(chars))

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
print("Número de palabras reservadas:", countRes)
print("Número de delimitadores en el código:", countDel)
print("Número de operadores en el código:", countOpe)
print("Número de contenedores en el código:", countCont)
print("Constantes encontradas en el código:", countConst)
for i, c in enumerate(constantes, 1):
    print(f'{i}: {c}')
