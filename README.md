# 🔢 Convertidor de Números con Árbol de Análisis Sintáctico

Este proyecto implementa un convertidor de números utilizando análisis léxico y sintáctico con PLY (Python Lex-Yacc), y una interfaz gráfica hecha con Tkinter. Permite convertir números decimales a distintos formatos: **romano, binario, octal, hexadecimal, palabra** (en español) y **aleatorio**, mostrando además el **árbol sintáctico** correspondiente a cada conversión.

---

## 🧠 Características

- ✅ Análisis léxico y sintáctico con PLY  
- ✅ Conversión de números decimales a múltiples formatos  
- ✅ Representación del árbol sintáctico  
- ✅ Interfaz gráfica moderna con Tkinter  
- ✅ Exportación automática de resultados a PDF  
- ✅ Manejo de errores léxicos y sintácticos  

---

## 💻 Tecnologías utilizadas

- Python 3.x  
- [PLY](https://www.dabeaz.com/ply/) – Lex/Yacc para Python  
- Tkinter – GUI nativa de Python  
- ReportLab – Generación de PDF  
- Unicode – Soporte para números romanos extendidos  

---

## 🧪 Formatos de conversión soportados

- `ROMANO` → Números romanos (con soporte extendido hasta millones)  
- `BINARIO` → Representación binaria  
- `OCTAL` → Representación octal  
- `HEXADECIMAL` → Representación hexadecimal  
- `PALABRA` → Texto en español  
- `ALEATORIO` → Una conversión aleatoria entre las anteriores  

---

## 📄 Ejemplo de salida (texto)
```
Cadena: 1024    => Salida (ROMANO): MXXIV
Árbol Sintáctico:
└── Producción: Simbolo_inicial
    ├── Número: 1024 (Tipo: NUMERO_DECIMAL)
    ├── Conversión: ROMANO (Tipo: ROMANO)
    └── Fin: $ (Tipo: FIN_ENTRADA)
```

---

## 📝 Ejemplo de entrada válida
```
1024 ROMANO $
58 BINARIO $
999 PALABRA $
100 ALEATORIO $
```

---

## 👨‍💻 Autor
Jairo Raudales


