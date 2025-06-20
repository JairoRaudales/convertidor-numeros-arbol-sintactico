""" CONVERTIDOR DE NÚMEROS CON ÁRBOL DE ANÁLISIS SINTÁCTICO """
import tkinter as tk
from tkinter import filedialog
from ply import lex, yacc
from random import randint
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import unicodedata
from reportlab.lib.units import inch

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

reset_linea = 0

#   DEFINICION DE TOKENS

# Nombres de tokens
tokens = (
    'NUMERO_DECIMAL',
    'ROMANO',
    'BINARIO',
    'OCTAL',
    'HEXADECIMAL',
    'PALABRA',
    'ALEATORIO',
    'FIN_ENTRADA',
)
# Expresiones regulares para los tokens
def t_NUMERO_DECIMAL(t):
    r'\d+'
    t.value = int(t.value)
    detalles_lexico.append("{:<6} | {:<20} | {:<20} |".format(t.lineno, t.type, t.value))
    return t

def t_ROMANO(t):
    r'ROMANO'
    detalles_lexico.append("{:<6} | {:<20} | {:<20} |".format(t.lineno, t.type, t.value))
    return t

def t_BINARIO(t):
    r'BINARIO'
    detalles_lexico.append("{:<6} | {:<20} | {:<20} |".format(t.lineno, t.type, t.value))
    return t

def t_OCTAL(t):
    r'OCTAL'
    detalles_lexico.append("{:<6} | {:<20} | {:<20} |".format(t.lineno, t.type, t.value))
    return t

def t_HEXADECIMAL(t):
    r'HEXADECIMAL'
    detalles_lexico.append("{:<6} | {:<20} | {:<20} |".format(t.lineno, t.type, t.value))
    return t

def t_PALABRA(t):
    r'PALABRA'
    detalles_lexico.append("{:<6} | {:<20} | {:<20} |".format(t.lineno, t.type, t.value))
    return t

def t_FIN_ENTRADA(t):
    r'\$'
    detalles_lexico.append("{:<6} | {:<20} | {:<20} |".format(t.lineno, t.type, t.value))
    return t

def t_ALEATORIO(t):
    r'ALEATORIO'
    detalles_lexico.append("{:<6} | {:<20} | {:<20} |".format(t.lineno, t.type, t.value))
    return t

def newline(t):
    r'\n'

t_ignore = ' \t'

#verifica si solo esta el encabezado antes de agregar errores
def t_error(t):
    if len(errores_lexicos) == 1:  # Solo contiene el encabezado
        errores_lexicos.append(f"Caracter inválido '{t.value[0]}' en la linea: {t.lexer.lineno}")
    else:
        errores_lexicos.append(f"Caracter inválido '{t.value[0]}' en la linea: {t.lexer.lineno}")
    t.lexer.skip(1)

# DEFINICIÓN DE LA GRAMÁTICA
def p_gramatica(p):
    """ 
    Simbolo_inicial : NUMERO_DECIMAL ROMANO FIN_ENTRADA
                    | NUMERO_DECIMAL BINARIO FIN_ENTRADA
                    | NUMERO_DECIMAL OCTAL FIN_ENTRADA
                    | NUMERO_DECIMAL HEXADECIMAL FIN_ENTRADA
                    | NUMERO_DECIMAL PALABRA FIN_ENTRADA
                    | NUMERO_DECIMAL ALEATORIO FIN_ENTRADA
    """
    try:
        numero_base_diez = p[1]
        destino = p[2]
        resultado = ''
        aleatorio = ''

        # Realizar la conversión basada en el tipo de destino
        if destino == 'ROMANO':
            resultado = numero_a_romano(numero_base_diez)
        elif destino == 'BINARIO':
            resultado = bin(numero_base_diez)[2:]
        elif destino == 'OCTAL':
            resultado = oct(numero_base_diez)[2:]
        elif destino == 'HEXADECIMAL':
            resultado = hex(numero_base_diez).upper()[2:]
        elif destino == 'PALABRA':
            resultado = numero_a_palabra(numero_base_diez)
        elif destino == 'ALEATORIO':
            tipos = ['ROMANO', 'BINARIO', 'OCTAL', 'HEXADECIMAL', 'PALABRA']
            aleatorio = tipos[randint(0, len(tipos)-1)]
            
            if aleatorio == 'ROMANO':
                resultado = numero_a_romano(numero_base_diez)
            elif aleatorio == 'BINARIO':
                resultado = bin(numero_base_diez)[2:]
            elif aleatorio == 'OCTAL':
                resultado = oct(numero_base_diez)[2:]
            elif aleatorio == 'HEXADECIMAL':
                resultado = hex(numero_base_diez).upper()[2:]
            elif aleatorio == 'PALABRA':
                resultado = numero_a_palabra(numero_base_diez)

        # Construccion de árbol sintáctico
        tree_lines = [
            "Árbol Sintáctico:",
            f"└── Producción: {p.slice[0].type}",
            f"    ├── Número: {p[1]} (Tipo: {p.slice[1].type})",
            f"    ├── Conversión: {p[2]} (Tipo: {p.slice[2].type})",
            f"    └── Fin: {p[3]} (Tipo: {p.slice[3].type})"
        ] 

        tree_message = "\n".join(tree_lines)

        # Mostrar resultados evitando duplicados
        output_str = f"Cadena: {numero_base_diez}\t=> Salida ({destino if not aleatorio else 'ALEATORIO->'+aleatorio}): {resultado}"
        
        if not hasattr(p_gramatica, "resultados_previos"):
            p_gramatica.resultados_previos = set()
        
        if output_str not in p_gramatica.resultados_previos:
            p_gramatica.resultados_previos.add(output_str)
            resultados.append(output_str)
            resultados.append(tree_message)

    #°envio de resultados(conversiones) a la interfaz
    except Exception as e:
        error_msg = f"Error en línea {p.lineno}: {str(e)}"
        if not hasattr(p_gramatica, "errores_mostrados"):
            p_gramatica.errores_mostrados = set()
        
        if error_msg not in p_gramatica.errores_mostrados:
            p_gramatica.errores_mostrados.add(error_msg)
            resultados.append(error_msg)

# CONVERTIR DE NÚMEROS DECIMALES A NUMEROS ROMANOS

def numero_a_romano(numero):
    """Funcion para convertir números decimales a número romanos"""
    if numero <= 0:
        return f"No es posible convertir {numero} a romano"
    
    valores_base = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'),
        (1, 'I')
    ]
    
    resultado = []

    if numero > 3999:
        miles = numero // 1000
        resto = numero % 1000
        
        romano_miles = []
        for valor, simbolo in valores_base:
            while miles >= valor:
                simbolo_con_vinculum = ''.join([f"{c}\u0305" for c in simbolo])
                romano_miles.append(simbolo_con_vinculum)
                miles -= valor
        
        romano_resto = []
        for valor, simbolo in valores_base:
            while resto >= valor:
                romano_resto.append(simbolo)
                resto -= valor
        
        return ''.join(romano_miles) + ''.join(romano_resto)
    
    for valor, simbolo in valores_base:
        while numero >= valor:
            resultado.append(simbolo)
            numero -= valor

    return ''.join(resultado)

#  CONVERTIR DE NÚMEROS A PALABRAS

def numero_a_palabra(number):
    """Función para convertir números decimales a palabras"""
    UNIDADES = [
        'cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 
        'seis', 'siete', 'ocho', 'nueve'
    ]

    DIEZ_A_19 = [
        'diez', 'once', 'doce', 'trece', 'catorce', 'quince',
        'dieciseis', 'diecisiete', 'dieciocho', 'diecinueve'
    ]

    DIECES = [
        'cero', 'diez', 'veinte', 'treinta', 'cuarenta', 
        'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa'
    ]

    CIENES = [
        '', 'ciento', 'doscientos', 'trescientos', 'cuatroscientos',
        'quinientos', 'seiscientos', 'setecientos', 'ochocientos', 'novecientos'
    ]

    def convertir_decenas(numero):
        if numero == 0:
            return 'cero'
        if numero < 10:
            return UNIDADES[numero]
        decenas, unidad = divmod(numero, 10)
        if numero <= 19:
            return DIEZ_A_19[unidad]
        elif numero <= 29:
            return f'veinti{UNIDADES[unidad]}'
        else:
            resultado = DIECES[decenas]
            if unidad > 0:
                resultado = f'{resultado} y {UNIDADES[unidad]}'
            return resultado

    def convertir_centenas(numero):
        centena, decenas = divmod(numero, 100)
        if decenas == 0:
            if centena == 1:
                return 'cien'
            else: 
                return CIENES[centena]
        else:
            resultado = CIENES[centena]
            if decenas > 0:
                resultado = f'{resultado} {convertir_decenas(decenas)}'
            return resultado

    def convertir_miles(numero):
        millar, centena = divmod(numero, 1000)
        resultado = ''
        if (millar == 1):
            resultado = 'mil'
        if (millar >= 2) and (millar <= 9):
            resultado = UNIDADES[millar] + ' mil'
        elif (millar >= 10) and (millar <= 99):
            resultado = convertir_decenas(millar) + ' mil'
        elif (millar >= 100) and (millar <= 999):
            resultado = convertir_centenas(millar) + ' mil'
        if centena > 0:
            resultado = f'{resultado} {convertir_centenas(centena)}'
        return resultado

    def convertir_millones(numero):
        millon, millar = divmod(numero, 1000000)
        resultado = ''
        if (millon == 1):
            resultado = 'un millón'
        if (millon >= 2) and (millon <= 9):
            resultado = UNIDADES[millon] + ' millones'
        elif (millon >= 10) and (millon <= 99):
            resultado = convertir_decenas(millon) + ' millones'
        elif (millon >= 100) and (millon <= 999):
            resultado = convertir_centenas(millon) + ' millones'
        if (millar > 0) and (millar <= 999):
            resultado = f'{resultado} {convertir_centenas(millar)}'
        elif (millar >= 1000) and (millar <= 999999):
            resultado = f'{resultado} {convertir_miles(millar)}'
        return resultado

    if number == 0:
        return 'cero'

    return convertir_millones(number)

# INTERFAZ GRÁFICA
class Convertidor:
    def __init__(self, root):
        self.root = root
        self.root.title("🔢 Convertidor de Números")
        self.root.geometry("1000x600")
        self.root.configure(bg="#121212")

        fuente_base = ("Segoe UI", 10)
        color_fondo = "#1E1E1E"
        color_texto = "#F5F5F5"
        color_acento = "#FA8072"
        color_borde = "#2E2E2E"

        # ========= ENTRADA =========
        entrada_frame = tk.Frame(root, bg=color_fondo, bd=2, relief="ridge")
        entrada_frame.pack(padx=20, pady=20, fill="x")

        tk.Label(entrada_frame, text="📝 Entrada:", font=("Segoe UI", 12, "bold"), fg="#61dafb", bg=color_fondo).pack(anchor="w", pady=(5, 0))
        self.entrada = tk.Text(entrada_frame, height=6, bg="#252526", fg=color_texto, insertbackground=color_texto,
                               font=("Consolas", 11), relief="flat", bd=2)
        self.entrada.pack(fill="x", pady=10, padx=10)

        # ========= BOTONES =========
        botones_frame = tk.Frame(root, bg=color_fondo)
        botones_frame.pack(pady=(0, 20))

        self._boton_estilizado(botones_frame, "📂 Abrir archivo", self.abrir_archivo, "#4FC3F7", "#039BE5").pack(side="left", padx=15)
        self._boton_estilizado(botones_frame, "🔄 Traducir", self.cargar_resultados, "#81C784", "#43A047").pack(side="left", padx=15)
        self._boton_estilizado(botones_frame, "🧹 Limpiar todo", self.limpiar_todo, "#EF9A9A", "#E53935").pack(side="left", padx=15)

        # ========= RESULTADOS =========
        resultados_frame = tk.Frame(root, bg=color_fondo)
        resultados_frame.pack(padx=20, pady=(0, 20), fill="both", expand=True)

        frame_lex = tk.Frame(resultados_frame, bg=color_fondo, bd=2, relief="ridge")
        frame_lex.pack(side="left", expand=True, fill="both", padx=(0, 10))

        tk.Label(frame_lex, text="🔍 Análisis Léxico", font=("Segoe UI", 11, "bold"), fg="#FFD54F", bg=color_fondo).pack(anchor="w", padx=10, pady=(5, 0))
        self.detalles_AL = tk.Text(frame_lex, bg="#1F1F1F", fg=color_texto, insertbackground=color_texto,
                                   font=("Consolas", 10), relief="flat", bd=2, state='disabled')
        self.detalles_AL.pack(fill="both", expand=True, padx=10, pady=5)

        frame_sint = tk.Frame(resultados_frame, bg=color_fondo, bd=2, relief="ridge")
        frame_sint.pack(side="left", expand=True, fill="both")

        tk.Label(frame_sint, text="🧠 Análisis Sintáctico", font=("Segoe UI", 11, "bold"), fg="#FFD54F", bg=color_fondo).pack(anchor="w", padx=10, pady=(5, 0))
        self.text_resultado = tk.Text(frame_sint, bg="#1F1F1F", fg=color_texto, insertbackground=color_texto,
                                      font=("Consolas", 10), relief="flat", bd=2, state='disabled')
        self.text_resultado.pack(fill="both", expand=True, padx=10, pady=5)

        # Iniciar lexer y parser (solo ejemplo, debes definir los tuyos)
        self.lexer = lex.lex()
        self.parser = yacc.yacc()

    def _boton_estilizado(self, parent, texto, comando, color_fondo, hover_color):
        btn = tk.Button(parent, text=texto, command=comando,
                        bg=color_fondo, fg="#000000",
                        font=("Segoe UI", 10, "bold"),
                        relief="flat", activeforeground="#000",
                        padx=15, pady=7, bd=0, cursor="hand2")

        def on_enter(e):
            btn.configure(bg=hover_color)

        def on_leave(e):
            btn.configure(bg=color_fondo)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def abrir_archivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                contenido_entrada = file.read()
                self.entrada.config(state="normal")
                self.entrada.delete(1.0, tk.END)
                self.entrada.insert(tk.END, contenido_entrada)

    def traducir_entradas(self, input_string):
        lineas = input_string.split('\n')
        resultados = []
        for index, linea in enumerate(lineas):
            if linea.strip():  # Ignorar líneas en blanco
                result = self.traducir(linea, index)
                resultados.append(result)
        return "\n".join(resultados)
    
    def limpiar_texto(self, texto):
        texto = texto.replace('\t', '    ')  # Reemplazar tabulaciones con espacios
        return ''.join(
            c if unicodedata.category(c)[0] != 'C' or c == '\n' else ' '
            for c in texto
    )

    def generar_pdf(self, entrada, lexico, errores, sintactico):

        ruta = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not ruta:
            return
        
        pdfmetrics.registerFont(TTFont('DejaVuSansMono', os.path.join('DejaVuSansMono.ttf')))

        c = canvas.Canvas(ruta, pagesize=letter)
        width, height = letter

        y = height - inch
        x = inch * 0.75

        def dibujar_texto(titulo, contenido, y_actual):
            c.setFont("Helvetica-Bold", 11)
            c.drawString(x, y_actual, f"■ {titulo}:")
            y_actual -= 14

            c.setFont("DejaVuSansMono", 9)
            for linea in contenido.split('\n'):
                c.drawString(x, y_actual, linea)
                y_actual -= 11
                """ if y_actual < 50:
                    c.showPage()
                    y_actual = height - inch """
                
                if y_actual < 50:
                    c.showPage()
                    c.setFont("DejaVuSansMono", 9)  # Reestablecer fuente tras cambio de página
                    y_actual = height - inch


            return y_actual - 10

        entrada = self.limpiar_texto(entrada)
        lexico = self.limpiar_texto(lexico)
        errores = self.limpiar_texto(errores)
        sintactico = self.limpiar_texto(sintactico)

        y = dibujar_texto("Entrada del usuario", entrada, y)
        y = dibujar_texto("Análisis Léxico", lexico, y)
        y = dibujar_texto("Errores Léxicos", errores, y)
        y = dibujar_texto("Análisis Sintáctico", sintactico, y)

        c.save()

    def cargar_resultados(self):
        input_string = self.entrada.get(1.0, 'end-1c')

        global detalles_lexico, errores_lexicos, reset_linea
        reset_linea = 1

        detalles_lexico = []
        cabecera = f"{'Línea':<6} | {'Tipo de token':<20} | {'Valor del token':<20} |"
        separador = "=" * len(cabecera)

        errores_lexicos = ['=====================================================|\n\nErrores léxicos:']
        errores_lexicos.append('No se han encontrado errores en el análisis léxico')

        detalles_lexico.append(separador)
        detalles_lexico.append(cabecera)
        detalles_lexico.append(separador)
        
        translated_result = self.traducir_entradas(input_string)

        # Mostrar detalles léxicos
        self.detalles_AL.config(state="normal")
        self.detalles_AL.delete(1.0, tk.END)
        self.detalles_AL.insert(tk.END, "\n".join(detalles_lexico))
        self.detalles_AL.insert(tk.END, "\n\n" + "\n".join(errores_lexicos))
        self.detalles_AL.config(state="disabled")

        # Mostrar resultados sintácticos
        self.text_resultado.config(state="normal")
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.insert(tk.END, translated_result)
        self.text_resultado.config(state="disabled")

        # Generar PDF automáticamente
        entrada_txt = self.entrada.get(1.0, 'end-1c')
        lexico_txt = "\n".join(detalles_lexico)
        errores_txt = "\n".join(errores_lexicos)
        sintactico_txt = translated_result

        self.generar_pdf(entrada_txt, lexico_txt, errores_txt, sintactico_txt)

    def traducir(self, input_line, index):
        global resultados
        resultados = []

        self.lexer.lineno = index + 1
        self.parser.parse(input_line, lexer=self.lexer)

        return "\n".join(resultados)

    def limpiar_todo(self):
        # Limpiar entrada
        self.entrada.config(state="normal")
        self.entrada.delete(1.0, tk.END)

        # Limpiar análisis léxico
        self.detalles_AL.config(state="normal")
        self.detalles_AL.delete(1.0, tk.END)
        self.detalles_AL.config(state="disabled")

        # Limpiar análisis sintáctico
        self.text_resultado.config(state="normal")
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.config(state="disabled")

        # Reiniciar variables globales si se usan
        global detalles_lexico, errores_lexicos, resultados
        detalles_lexico = []
        errores_lexicos = []
        resultados = []

# INICIAR LA APLICACIÓN
if __name__ == "__main__":
    root = tk.Tk()
    app = Convertidor(root)
    root.mainloop()