# Analizador léxico y sintáctico simplificado 

# AFD para id
def afd_id(cadena):
    estado = 0
    i = 0
    while i < len(cadena):
        c = cadena[i]
        if estado == 0:
            if c.isalpha():
                estado = 1
            else:
                break
        elif estado == 1:
            if c.isalnum():
                estado = 1
            else:
                break
        i += 1
    if estado == 1:
        return i  # longitud del token válido
    return 0

# AFD para num con signo opcional
def afd_num(cadena):
    estado = 0
    i = 0
    while i < len(cadena):
        c = cadena[i]
        if estado == 0:
            if c in "+-":
                estado = 1
            elif c.isdigit():
                estado = 2
            else:
                break
        elif estado == 1:
            if c.isdigit():
                estado = 2
            else:
                break
        elif estado == 2:
            if c.isdigit():
                estado = 2
            else:
                break
        i += 1
    if estado == 2:
        return i  # longitud del token válido
    return 0

# AFD para operadores y paréntesis
def afd_op_par(cadena):
    if cadena and cadena[0] in "+-*/=()":
        return 1
    return 0

# Analizador léxico general 
def analizador_lexico(cadena):
    tokens = []
    i = 0
    while i < len(cadena):
        c = cadena[i]

        # Ignorar espacios en blanco
        if c.isspace():
            i += 1
            continue

        # Intentar id
        longitud = afd_id(cadena[i:])
        if longitud > 0:
            tokens.append(("id", cadena[i:i+longitud]))
            i += longitud
            continue

        # Intentar num
        longitud = afd_num(cadena[i:])
        if longitud > 0:
            tokens.append(("num", cadena[i:i+longitud]))
            i += longitud
            continue

        # Intentar operador o paréntesis
        longitud = afd_op_par(cadena[i:])
        if longitud > 0:
            tokens.append((cadena[i], cadena[i]))
            i += longitud
            continue

        # Si no entró en ningún AFD da error léxico
        raise ValueError(f"Error léxico: carácter no válido '{c}' en la posición {i}")

    return tokens

# Parser sintáctico recursivo
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Lista de tokens a analizar
        self.pos = 0          # Posición en la lista de tokens

    # Devuelve el token actual (o None si ya no hay más)
    def obtener_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    # Verifica si el token actual es del tipo esperado y avanza si si
    def coincidir(self, tipo):
        token = self.obtener_token()
        if token and token[0] == tipo:
            self.pos += 1
            return True
        return False

    # inicial S → id = E | E
    def S(self):
        if self.obtener_token() and self.obtener_token()[0] == 'id':
            self.coincidir('id')
            if self.coincidir('='):
                return self.E()
            return False  # Si no hay "=", no es válido
        else:
            return self.E()  # Si no es asignación, puede ser solo una expresión

    # E → T {(+|-) T}
    def E(self):
        if not self.T():  # Primero se espera un término
            return False
        while self.obtener_token() and self.obtener_token()[0] in ('+', '-'):
            self.coincidir(self.obtener_token()[0])  # Se consume el operador
            if not self.T():  # Debe haber otro término
                return False
        return True

    # T → F {(*|/) F}
    def T(self):
        if not self.F():  # Se espera un factor
            return False
        while self.obtener_token() and self.obtener_token()[0] in ('*', '/'):
            self.coincidir(self.obtener_token()[0])  # Se consume el operador
            if not self.F():  # Debe haber otro factor
                return False
        return True

    # F → id | num | (E)
    def F(self):
        token = self.obtener_token()
        if token is None:
            return False
        if token[0] == 'num':
            return self.coincidir('num')
        elif token[0] == 'id':
            return self.coincidir('id')
        elif token[0] == '(':
            self.coincidir('(')
            if not self.E():  # Dentro del paréntesis debe haber una expresión válida
                return False
            return self.coincidir(')')  # Cerramos el paréntesis
        return False  # Si no es ninguna de las opciones válidas te da error

    # Devuelve True si toda la expresión es válida
    def parsear(self):
        valido = self.S()
        return valido and self.obtener_token() is None  # Se asegura que no queden tokens sin procesar

# Imprimir resultados
def analizar_expresion(expresion):
    try:
        tokens = analizador_lexico(expresion)  # Se generan los tokens
        print("- Tokens:", tokens)
        parser = Parser(tokens)
        if parser.parsear():
            print("Expresión válida :)")  # Si pasa el parser, es correcta
        else:
            print("Error sintáctico :(")  # Si no, hay un error en el orden
    except ValueError as e:
        print(e)  # Si hay errores léxicos, se muestran

# Función con menú para ejecutar pruebas o ingresar expresiones personalizadas
def main():
    print("- Analizador de expresiones")
    print("1. Ejecutar casos de prueba")
    print("2. Ingresar nueva expresión")
    opcion = input("Selecciona una opción (1 o 2): ")

    if opcion == "1":
        # Lista de casos de prueba 
        casos = [
            "x = -3 + y / 2",                 # Válido
            "resultado = (a + b) * 2",        # Válido
            "x = + + 2",                      # Inválido (doble signo)
            "(3 + 2",                         # Inválido (falta paréntesis de cierre)
            "x = 3 @ 4"                       # Inválido (el caracter '@' no es válido)
        ]
        for idx, expr in enumerate(casos):
            print(f"\n Caso {idx + 1}: '{expr}'")
            analizar_expresion(expr)

    elif opcion == "2":
        # El usuario puede ingresar una expresión como input()
        entrada = input("Escribe una expresión: ")
        print("\n Analizando tu expresión:")
        analizar_expresion(entrada)

    else:
        # Validación del menú
        print("Opción no válida. Intenta con 1 o 2.")

main()
