import re

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

cpp_operador = {
    '+','++','*','<<','!=','&&','=','#','<','>'
}

cpp_contenedores = {
    '(',')','{','}'
}

# Clasificaciones
keywords = set()
countRes = 0

numbers = set ()
countNum = 0

delimit = set ()
countDel = 0

operador = set ()
countOpe = 0 

contenedor = set ()
countCont = 0

with open('archivo.cpp', 'r') as f:
    content = f.read()
    content = re.sub(r'//.*|/\*[\s\S]*?\*/', '', content)
    # Extrae las palabras
    words = re.findall(r'\b\w+\b|[;,.]', content) 

    for word in words:
        if word in cpp_keywords:
            keywords.add(word)
            countRes+=1
    
    for word in content:
        if word in cpp_keywords:
            keywords.add(word)
            countRes+=1
        if re.match(r'-?\b\d+(\.\d+)?\b', word):
            # -r para los numeros negativos
            # \b para asegurar que son numeros y que no viene pegado a una palabra
            # \d+ para los numeros de mas de 1 digito
            # (\.\d+)? para los decimales
            numbers.add(word)
            countNum+=1
        if word in cpp_end :
            delimit.add(word)
            countDel+=1
        if word in cpp_operador :
            operador.add(word)
            countOpe+=1
        if word in cpp_contenedores :
            contenedor.add(word)
            countCont+=1
        

print("Palabras reservadas:", sorted(keywords))
print("Numero de palabras reservadas: ", countRes) 
print("Numero de valores numericos en el codigo: ", countNum) #ME MARCA UN NUMERO MAS PERO NO SE DONDEEE 
print("Numero de delimitadores en el codigo: ", countDel) 
print("Numero de operadores en el codigo: ", countOpe) 
print("Numero de contenedores en el codigo: ", countCont)