import tkinter as tk
from tkinter import ttk
from preguntas import DATA
import json

class Pregunta:
    def __init__(self, dict_pregunta):
        self.enunciado = dict_pregunta["Pregunta"] # str
        self.respuestas = dict_pregunta["Opciones"] # list
        self.respuesta_correcta = dict_pregunta["Respuesta"] # int

    def getEnunciado(self): # none -> str
        return self.enunciado
    
    def getOpciones(self): # none -> list
        return self.respuestas
    
    def getRespuesta(self): # none -> int
        return self.respuesta_correcta

    def verificarRespuesta(self, respuesta): # str -> bool
        return self.respuestas.index(respuesta) == self.respuesta_correcta
    
num_pregunta = 0
puntos = 0
pregunta_actual = Pregunta(DATA[num_pregunta])

def iniciarQuiz():
    global nombre_usuario
    nombre_usuario = entrada_nombre.get()
    if nombre_usuario:
        pantalla_inicio.pack_forget()
        pantalla_quiz.pack(fill="both")
        mostrarPregunta()

def guardarPuntaje():
    puntajes = cargarPuntajes()
    puntajes.append({"nombre": nombre_usuario, "puntaje": puntos})
    with open("puntajes.json", "w") as file:
        json.dump(puntajes, file)

def cargarPuntajes():
    try:
        with open("puntajes.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def mostrarPuntajes():
    pantalla_quiz.pack_forget()
    pantalla_puntajes.pack(fill="both", expand=True)

    puntajes = cargarPuntajes()
    texto_puntajes = "\n".join([f"{p['nombre']}: {p['puntaje']}" for p in puntajes])
    lista_puntajes.configure(text=texto_puntajes)

def responderCorrecto():
    resultado.configure(text="¡Correcto!")
    resultado.pack()
    btn_siguiente.pack(pady=30)

    global puntos
    puntos += 1
    puntuacion.configure(text=f"Puntuación: {puntos}")
    
def responderIncorrecto():
    resultado.configure(text="Incorrecto")
    resultado.pack()
    
    btn_siguiente.pack(pady=30)

def siguientePregunta():
    global num_pregunta, pregunta_actual
    num_pregunta += 1

    if num_pregunta < len(DATA):
        pregunta_actual = Pregunta(DATA[num_pregunta])
        actualizarInterfaz()
    else:
        guardarPuntaje()
        mostrarPuntajes()

def actualizarInterfaz():
    resultado.configure(text="")
    for boton in botones_opciones:
        boton.pack_forget()

    enunciado.config(text=pregunta_actual.getEnunciado())
    botones_opciones.clear()

    for opcion in pregunta_actual.getOpciones():
        if pregunta_actual.verificarRespuesta(opcion):
            boton = ttk.Button(pantalla_quiz, command=responderCorrecto, text=opcion)
        else:
            boton = ttk.Button(pantalla_quiz, command=responderIncorrecto, text=opcion)
        boton.pack(pady=5)
        botones_opciones.append(boton)
    
    btn_siguiente.pack_forget()

def mostrarPregunta():
    puntuacion.place(relx=1, y=0, anchor="ne")

    enunciado.pack(pady=45)

    actualizarInterfaz()
    
def reiniciar():
    global num_pregunta, pregunta_actual
    num_pregunta = 0
    puntos = 0
    pregunta_actual = Pregunta(DATA[num_pregunta])
    actualizarInterfaz()
    
    pantalla_puntajes.pack_forget()
    pantalla_inicio.pack(fill="both")
    #mostrarPregunta()
            
ventana = tk.Tk()
ventana.title("PyQuiz") 
ventana.geometry('600x450')

# Pantalla de inicio
pantalla_inicio = ttk.Frame(ventana)
pantalla_inicio.pack(fill="both", expand=True)
ttk.Label(pantalla_inicio, text="Ingrese su nombre:").pack(pady=10)
entrada_nombre = ttk.Entry(pantalla_inicio)
entrada_nombre.pack(pady=10)
btn_iniciar = ttk.Button(pantalla_inicio, text="Iniciar", command=iniciarQuiz)
btn_iniciar.pack(pady=10)

# Pantalla del quiz
pantalla_quiz = ttk.Frame(ventana)

puntuacion = ttk.Label(pantalla_quiz, text=f"Puntuación: {puntos}")
puntuacion.pack(anchor="ne", padx=10, pady=10)
enunciado = ttk.Label(pantalla_quiz, text="")
enunciado.pack(pady=20)
resultado = ttk.Label(pantalla_quiz, text="")
resultado.pack()
btn_siguiente = ttk.Button(pantalla_quiz, command=siguientePregunta, text="Continuar")
botones_opciones = []

# Pantalla de puntajes
pantalla_puntajes = ttk.Frame(ventana)
ttk.Label(pantalla_puntajes, text="Puntajes:").pack(pady=10)
lista_puntajes = ttk.Label(pantalla_puntajes, text="")
lista_puntajes.pack(pady=10)
# reinicio
btn_reinicio = ttk.Button(pantalla_puntajes, command=reiniciar, text="Reiniciar")
btn_reinicio.pack(pady=40)

mostrarPregunta()

if __name__ == "__main__":
    ventana.mainloop()
