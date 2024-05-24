import tkinter as tk
from tkinter import ttk
from preguntas import DATA

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

def responderCorrecto():
    resultado.config(text="¡Correcto!")
    resultado.pack()
    btn_siguiente.pack(pady=55)
    global puntos
    puntos += 1
    puntacion.config(text=f"Puntuación: {puntos}")
    
def responderIncorrecto():
    resultado.config(text="Incorrecto")
    resultado.pack()

    btn_siguiente.pack(pady=55)

def siguientePregunta():
    pass

def mostrarPregunta():
    puntacion.place(relx=1, y=0, anchor="ne")

    enunciado.pack(pady=45)

    global botones_opciones
    botones_opciones = []

    opcion = 0
    for i in pregunta_actual.getOpciones():
        if pregunta_actual.verificarRespuesta(i):
            boton = ttk.Button(ventana, command=responderCorrecto, text=f"{i}")
        else: 
            boton = ttk.Button(ventana, command=responderIncorrecto, text=f"{i}")
        boton.pack(pady=10)
        botones_opciones.append(boton)
            

ventana = tk.Tk()
ventana.title("Pyquiz") 
ventana.geometry('600x450')

puntacion = ttk.Label(ventana, text=f"Puntuación: {puntos}")
enunciado = ttk.Label(ventana, text="¿Cuanto es 2 + 2?")
resultado = ttk.Label(ventana, text="")
btn_siguiente = ttk.Button(ventana, command=siguientePregunta, text="Continuar")

preguntas = []
for i in DATA:
    qstn = Pregunta(i)
    preguntas.append(qstn)

mostrarPregunta()

if __name__ == "__main__":
    ventana.mainloop()
