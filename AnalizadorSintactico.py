# analizador_sintactico.py

import re
import AnalizadorLexico
import os

def tokenizar(linea):
    patron = r'''
        "[^"]*"              |  # Cadenas
        '[^']'               |  # Caracteres
        \d+\.\d+             |  # Flotantes
        \d+                  |  # Enteros
        <<|>>|==|!=|<=|>=    |  # Operadores dobles
        [a-zA-Z_]\w*         |  # Identificadores
        [#@$%^&{}\[\]();<>=!+\-*/.,]  # Símbolos individuales (agregados corchetes)
    '''
    return re.findall(patron, linea, re.VERBOSE)

def analizar_cpp_palabra_a_palabra(ruta_archivo):
    extension = os.path.splitext(ruta_archivo)[1]
    es_cpp = extension == '.cpp'

    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    errores = []
    salida = [] 
    pila_llaves = []
    pila_par = []
    variables_declaradas = set()

    for i, linea in enumerate(lineas):
        linea_num = i + 1
        tokens = tokenizar(linea.strip())
        if not tokens:
            continue

        if linea.count('"') % 2 != 0:
            errores.append(f"Línea {linea_num}: Cadena de texto sin cerrar.")

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

        if 'main' in tokens:
            if 'int' not in tokens or '(' not in tokens or ')' not in tokens:
                errores.append(f"Línea {linea_num}: Declaración incorrecta de la función main.")

        if 'if' in tokens and ('(' not in tokens or ')' not in tokens):
            errores.append(f"Línea {linea_num}: 'if' sin paréntesis de condición.")

        if 'for' in tokens:
            if '(' not in tokens or ')' not in tokens:
                errores.append(f"Línea {linea_num}: 'for' sin paréntesis.")
            else:
                segmento = linea[linea.find('(')+1:linea.find(')')]
                if segmento.count(';') != 2:
                    errores.append(f"Línea {linea_num}: Estructura 'for' mal formada.")

        if 'cout' in linea:
            if linea.count('<<') % 2 != 0:
                errores.append(f"Línea {linea_num}: cout incorrecto, número impar de '<<'")

        if 'else' in tokens:
            if 'if' not in tokens and not any('if' in tokenizar(lineas[j].strip()) for j in range(max(0, i - 2), i)):
                errores.append(f"Línea {linea_num}: 'else' sin 'if' anterior.")

        estructuras_control = {'if', 'for', 'while', 'else', 'switch'}

        # -------------------------
        # Validación de arreglos
        # -------------------------
        # -------------------------
        # Validación de arreglos
        # -------------------------
        tipo = tokens[0] if tokens else ''
        if tipo in ['int', 'float', 'string', 'char'] and '[' in tokens and ']' in tokens:
            try:
                var_name = tokens[1]
                index_open = tokens.index('[')
                index_close = tokens.index(']')
                size_token = tokens[index_open + 1] if index_close == index_open + 2 else None

                # Validar nombre
                if var_name not in AnalizadorLexico.conteo_variables:
                    errores.append(f"Línea {linea_num}: nombre de variable de arreglo inválido")

                # Validar tamaño
                if size_token:
                    if not re.fullmatch(r'\d+', size_token):
                        errores.append(f"Línea {linea_num}: tamaño del arreglo inválido")
                else:
                    errores.append(f"Línea {linea_num}: tamaño del arreglo no especificado")

                # Validar finalización con ;
                if tokens[-1] != ';' and '=' not in tokens:
                    errores.append(f"Línea {linea_num}: declaración de arreglo no termina con ';'")

                # Validar inicialización si hay '='
                if '=' in tokens:
                    igual_index = tokens.index('=')
                    if tokens[igual_index + 1] != '{' or tokens[-2] != '}':
                        errores.append(f"Línea {linea_num}: inicialización de arreglo mal formada")

                if var_name in variables_declaradas:
                    errores.append(f"Línea {linea_num}: Arreglo '{var_name}' ya declarado anteriormente.")
                else:
                    variables_declaradas.add(var_name)
                continue  # saltar verificación adicional de variables

            except Exception:
                errores.append(f"Línea {linea_num}: error general en la declaración de arreglo")
                continue


        # Declaraciones de variables
        if len(tokens) >= 5 and tokens[0] in ['int', 'float', 'string', 'char']:
            tipo = tokens[0]
            var_name = tokens[1]
            operador_asign = tokens[2]
            valor = tokens[3]
            termina_con_puntoycoma = tokens[-1] == ';'

            if operador_asign != '=' or not termina_con_puntoycoma:
                errores.append(f"Línea {linea_num}: Declaración de {tipo} mal estructurada")
            else:
                if var_name not in AnalizadorLexico.conteo_variables:
                    errores.append(f"Línea {linea_num}: nombre de variable inválido")
                else:
                    if tipo == 'int' and not re.fullmatch(r'\d+', valor):
                        errores.append(f"Línea {linea_num}: El valor asignado no es un entero")
                    elif tipo == 'float' and not re.fullmatch(r'\d+\.\d+', valor):
                        errores.append(f"Línea {linea_num}: El valor asignado no es un flotante válido")
                    elif tipo == 'char':
                        if not re.fullmatch(r"'.{1}'", valor):
                            errores.append(f"Línea {linea_num}: El valor asignado no es un char válido")
                    elif tipo == 'string':
                        if not re.fullmatch(r'"[^"]*"', valor):
                            errores.append(f"Línea {linea_num}: El valor asignado no es un string válido")

                if var_name in variables_declaradas:
                    errores.append(f"Línea {linea_num}: Variable '{var_name}' ya declarada anteriormente.")
                else:
                    variables_declaradas.add(var_name)


        # Verificación de punto y coma
        if tokens:
            termina_con_puntoycoma = tokens[-1] == ';'
            comienza_con_estructura = tokens[0] in estructuras_control
            es_bloque = tokens[0] in ['{', '}', '#']
            es_declaracion_funcion = 'main' in tokens

            if not termina_con_puntoycoma and not comienza_con_estructura and not es_bloque and not es_declaracion_funcion:
                errores.append(f"Línea {linea_num}: Instrucción no termina con ';'")

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
    else:
        salida.append("Archivo sintácticamente correcto (nivel palabra a palabra básico).")

    return "\n".join(salida)
