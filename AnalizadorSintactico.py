import re
import AnalizadorLexico
import os

def tokenizar(linea):
    return re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|[#@$%^&{}();<>=!+\-*/.,]|"[^"]*"|<<|>>|==|!=|<=|>=', linea)

def analizar_cpp_palabra_a_palabra(ruta_archivo):
    extension = os.path.splitext(ruta_archivo)[1]
    es_cpp = extension == '.cpp'

    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    errores = []
    salida = [] 
    pila_llaves = []
    pila_par = []
    linea_num = 0
    variables_declaradas = set()

    for i, linea in enumerate(lineas):
        linea_num = i + 1
        tokens = tokenizar(linea.strip())
        if not tokens:
            continue

        print(f"Línea {linea_num}: {tokens}")

        #VALIDACION COMILLAS
        if linea.count('"') % 2 != 0:
            errores.append(f"Línea {linea_num}: Cadena de texto sin cerrar.")

        #VALIDACION LIBRERIA SI ES .CPP
        if linea_num == 1:
            print("ENTRE AL IF")
            if es_cpp:
                if len(tokens) >= 5 and tokens[:5] == ['#', 'include', '<', 'iostream', '>']:
                    print("Librería válida detectada (C++).")
                else:
                    errores.append(f"Línea {linea_num}: '#include <iostream>' mal formado / escrito (esperado en C++)")
            else:
                if len(tokens) >= 7 and tokens[:7] == ['#', 'include', '<', 'stdio', '.', 'h', '>']:
                    print("Librería válida detectada (C).")
                else:
                    errores.append(f"Línea {linea_num}: '#include <stdio.h>' mal formado / escrito (esperado en C)")
        #VALIDACION SI ES .C
        if linea_num == 2:
            if es_cpp:
                if len(tokens) >= 4 and tokens[:4] == ['using', 'namespace', 'std', ';']:
                    print("Namespace válido detectado (C++).")
                else:
                    errores.append(f"Línea {linea_num}: 'using namespace std;' mal formado / escrito (esperado en C++)")
            else:
                # En C no se espera esta línea
                pass



        # Balance de llaves y paréntesis
        for token in tokens:
            if token == '{':
                pila_llaves.append('{')
            elif token == '}':
                if pila_llaves:
                    pila_llaves.pop()
                else:
                    errores.append(f"Línea {linea_num}: llave '}}' sin abrir.")
            elif token == '(':
                pila_par.append('(')
            elif token == ')':
                if pila_par:
                    pila_par.pop()
                else:
                    errores.append(f"Línea {linea_num}: paréntesis ')' sin abrir.")

        # Validación de main
        if 'main' in tokens:
            if 'int' not in tokens or '(' not in tokens or ')' not in tokens or '{' not in tokens:
                errores.append(f"Línea {linea_num}: Declaración incorrecta de la función main.")

        # Validación de if
        if 'if' in tokens:
            if '(' not in tokens or ')' not in tokens:
                errores.append(f"Línea {linea_num}: 'if' sin paréntesis de condición.")

        # Validación de for
        if 'for' in tokens:
            if '(' not in tokens or ')' not in tokens:
                errores.append(f"Línea {linea_num}: 'for' sin paréntesis.")
            else:
                segmento = linea[linea.find('(')+1:linea.find(')')]
                if segmento.count(';') != 2:
                    errores.append(f"Línea {linea_num}: Estructura 'for' mal formada.")

        # Validación de cadenas de texto
        if linea.count('"') % 2 != 0:
            errores.append(f"Línea {linea_num}: Cadena de texto sin cerrar.")

        # Validación cout con <<
        if 'cout' in tokens:
            couts = tokens.count('<')
            if couts % 2 != 0:
                errores.append(f"Línea {linea_num}: cout incorrecto, número impar de '<<'")

        # Validación else sin if reciente
        if 'else' in tokens:
            if 'if' not in tokens and not any('if' in tokenizar(lineas[j].strip()) for j in range(max(0, i - 2), i)):
                errores.append(f"Línea {linea_num}: 'else' sin 'if' anterior.")

        estructuras_control = {'if', 'for', 'while', 'else', 'switch'}

        if tokens:
            termina_con_puntoycoma = tokens[-1] == ';'
            comienza_con_estructura = tokens[0] in estructuras_control
            es_bloque = tokens[0] in ['{', '}', '#']
            es_declaracion_funcion = 'main' in tokens or ('(' in tokens and '{' in tokens)

            if not termina_con_puntoycoma and not comienza_con_estructura and not es_bloque and not es_declaracion_funcion:
                errores.append(f"Línea {linea_num}: Instrucción no termina con ';'")

        # Registrar variables declaradas y detectar duplicadas
        tipos = ['int', 'float', 'char', 'bool', 'double', 'string']
        if any(tipo in tokens for tipo in tipos):
            tipo_idx = next((i for i, t in enumerate(tokens) if t in tipos), -1)
            if tipo_idx != -1 and tipo_idx + 1 < len(tokens):
                nombre_var = tokens[tipo_idx + 1]
                if re.match(r'[a-zA-Z_]\w*', nombre_var):
                    if nombre_var in variables_declaradas:
                        errores.append(f"Línea {linea_num}: Variable '{nombre_var}' ya declarada anteriormente.")
                    else:
                        variables_declaradas.add(nombre_var)

        # Verificación de identificadores desconocidos
        for token in tokens:
            if re.match(r'[a-zA-Z_]\w*', token):
                if token not in AnalizadorLexico.keywords and \
                token not in AnalizadorLexico.delimit and \
                token not in AnalizadorLexico.operador and \
                token not in AnalizadorLexico.contenedor and \
                token not in AnalizadorLexico.constantes and \
                token not in AnalizadorLexico.conteo_variables and \
                token not in variables_declaradas:
                    errores.append(f"Línea {linea_num}: Identificador no declarado o inválido: '{token}'")

    if pila_llaves:
        errores.append("Error: hay llaves sin cerrar.")
    if pila_par:
        errores.append("Error: hay paréntesis sin cerrar.")

    if errores:
        salida.append("Errores encontrados:")
        salida.extend(errores)
        print("\nErrores encontrados:")
        for error in errores:
            print(error)
    else:
        print("\nArchivo sintácticamente correcto (nivel palabra a palabra básico).")
        salida.append("Archivo sintácticamente correcto (nivel palabra a palabra básico).")

    return "\n".join(salida)