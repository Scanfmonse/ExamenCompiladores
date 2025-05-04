import re

def tokenizar(linea):
    # Separa palabras y símbolos importantes como tokens individuales
    return re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|[#{}();<>=!+\-*/]|"[^"]*"|<<|>>|==|!=|<=|>=', linea)

def analizar_cpp_palabra_a_palabra(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    errores = []
    pila_llaves = []
    linea_num = 0

    for linea in lineas:
        linea_num += 1
        tokens = tokenizar(linea.strip())
        if not tokens:
            continue

        # Imprimir tokens para análisis (puedes quitarlo si no lo necesitas)
        print(f"Línea {linea_num}: {tokens}")

        #Para confirmar que el archivo si tenga librerias
        if linea_num == 1 :
            if len(tokens) >= 5:
                if tokens[0] == "#" and tokens[1] == 'include' and tokens[2] == '<' and tokens[3] == 'iostream' and tokens[4] == '>':
                    print("Librería válida detectada.")
                else:
                    errores.append(f"Línea {linea_num + 1}: '#include <iostream>' mal formado / escrito")
            else:
                errores.append(f"Línea {linea_num + 1}: No hay libreria declarada")

        if linea_num == 2 :
            if len(tokens) >= 4:
                if tokens[0] == 'using' and tokens[1] == 'namespace' and tokens[2] == 'std' and tokens[3] == ';' :
                    print("Librería válida detectada2")
                else:
                    errores.append(f"Línea {linea_num + 1}: 'using namespace std;' mal formado / escrito")
            else:
                errores.append(f"Línea {linea_num + 1}: No hay namespace declarado")


        #Que cada llave lleve su cierre
        for token in tokens:
            if token == "{":
                pila_llaves.append("{")
            elif token == "}":
                if pila_llaves:
                    pila_llaves.pop()
                else:
                    errores.append(f"Línea {linea_num}: llave '}}' sin abrir.")

        #Ver si hay algun if sin parentsesis
        if 'if' in tokens:
            if "(" not in tokens or ")" not in tokens:
                errores.append(f"Línea {linea_num}: 'if' sin paréntesis de condición.")

    #Ver si quedaron llaves abiertas
    if pila_llaves:
        errores.append("Error: hay llaves sin cerrar.")

    # Resultado
    if errores:
        print("\nErrores encontrados:")
        for error in errores:
            print(error)
    else:
        print("\nArchivo sintácticamente correcto (nivel palabra a palabra básico).")

# Prueba
analizar_cpp_palabra_a_palabra("archivo.cpp")
