import tkinter as tk
from tkinter import ttk
from preguntas import DATA
import json
import random as rd

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
    
puntos = 0
preguntas_ronda = DATA.copy()
temp_pregunta = rd.choice(preguntas_ronda)
pregunta_actual = Pregunta(temp_pregunta)

def iniciarQuiz():
    global nombre_usuario
    nombre_usuario = entrada_nombre.get()
    if (nombre_usuario != "admin") and (nombre_usuario != ""):
        pantalla_inicio.pack_forget()
        pantalla_quiz.pack(fill="both")
        mostrarPregunta()
        mostrarJugador()
    elif nombre_usuario == "admin":
        btn_admin = ttk.Button(pantalla_inicio, text="admin")
        btn_admin.pack(pady=10)
        ttk.Label(pantalla_inicio, text="Esto aún no hace nada xd", font=("Arial", 8, "italic")).pack()

def guardarPuntaje():
    puntajes = cargarPuntajes()
    puntajes.append({"nombre": nombre_usuario, "puntaje": puntos})
    with open("puntajes.json", "w") as file: # "w" = write
        json.dump(puntajes, file) # para escribir sobre el .json

def cargarPuntajes():
    try:
        with open("puntajes.json", "r") as file: # "r" = read
            return json.load(file) # se carga el contenido del .json y lo muestra
    except FileNotFoundError:
        return []
    
def jugar():
    pantalla_principal.pack_forget()
    pantalla_inicio.pack(fill="both", expand=True)

def mostrarPuntajes():
    pantalla_quiz.pack_forget()
    pantalla_principal.pack_forget()
    pantalla_puntajes.pack(fill="both", expand=True)

    puntajes = cargarPuntajes()
    puntajes_ordenados = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)[:10] # se ordenan los 10 mejores puntajes de forma descendente
    texto_puntajes = "\n".join([f"{i+1}. {p['nombre']}: {p['puntaje']}" for i, p in enumerate(puntajes_ordenados)]) # se muestran los puntajes enumerados
    lista_puntajes.configure(text=texto_puntajes)

def responderCorrecto():
    resultado.configure(text="¡Correcto!")
    resultado.pack()
    btn_siguiente.pack(pady=30)
    desactivarBotones()

    global puntos
    puntos += 1
    puntuacion.configure(text=f"Puntuación: {puntos}")
    
def responderIncorrecto():
    resultado.configure(text="Incorrecto")
    resultado.pack()
    btn_siguiente.pack(pady=30)
    desactivarBotones()

    global puntos
    puntos -= 1
    puntuacion.configure(text=f"Puntuación: {puntos}")

def desactivarBotones():
    for boton in botones_opciones:
        boton.state(['disabled']) # se cambia el estado del botón a "desactivado"

def siguientePregunta():
    global preguntas_ronda, pregunta_actual, temp_pregunta
    
    print("Preguntas antes de remover:", len(preguntas_ronda))
    print("Pregunta a remover:", temp_pregunta)
    
    if temp_pregunta in preguntas_ronda:
        preguntas_ronda.remove(temp_pregunta)
        print("Pregunta removida")
    else:
        print("Pregunta no encontrada en preguntas_ronda")
        
    print("Preguntas después de remover:", len(preguntas_ronda))

    if len(preguntas_ronda) != 0:
        temp_pregunta = rd.choice(preguntas_ronda)
        pregunta_actual = Pregunta(temp_pregunta)
        actualizarInterfaz()
    else:
        guardarPuntaje()
        mostrarPuntajes()


def actualizarInterfaz():
    resultado.configure(text="")
    for boton in botones_opciones:
        boton.pack_forget()

    enunciado.configure(text=pregunta_actual.getEnunciado())
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
    puntuacion.place(relx=1, x=-10, y=10, anchor="ne")
    enunciado.pack(pady=45)

    actualizarInterfaz()
    
def reiniciar():
    global pregunta_actual, puntos, preguntas_ronda, temp_pregunta

    preguntas_ronda = DATA.copy()
    temp_pregunta = rd.choice(preguntas_ronda)
    pregunta_actual = Pregunta(temp_pregunta)

    puntos = 0
    
    puntuacion.configure(text=f"Puntuación: {puntos}")
    actualizarInterfaz()
    
    pantalla_puntajes.pack_forget()
    pantalla_inicio.pack(fill="both")

def mostrarJugador():
    jugador.configure(text=f"Jugador: {nombre_usuario}")
    jugador.place(x=10, y=10, anchor="nw")
            
ventana = tk.Tk()
ventana.title("PyQuiz") 
ventana.geometry('600x450')
ventana.iconbitmap("necoarc.ico") # imagen original: https://www.deviantart.com/a-ngl/art/Neco-Arc-Emote-925437130

# Pantalla principal
pantalla_principal = ttk.Frame(ventana)
pantalla_principal.pack(fill="both", expand=True)
ttk.Label(pantalla_principal, text="PyQuiz", font=("Arial", 25, "bold")).pack(pady=50)
#ttk.Label(pantalla_principal, text=":DDDDDD", font=("Arial", 8)).pack()
btn_jugar = ttk.Button(pantalla_principal, text="Jugar", command=jugar)
btn_jugar.pack(pady=10)

btn_puntajes = ttk.Button(pantalla_principal, text="Ver puntajes", command=mostrarPuntajes)
btn_puntajes.pack()

# Pantalla de inicio
pantalla_inicio = ttk.Frame(ventana)
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

jugador = ttk.Label(pantalla_quiz, text="")
jugador.pack(pady=10)

#btn_salir = ttk.Button(pantalla_quiz, text="Salir", command=iniciarQuiz)
#btn_salir.pack()

# Pantalla de puntajes
pantalla_puntajes = ttk.Frame(ventana)
ttk.Label(pantalla_puntajes, text="Puntajes:").pack(pady=10)
lista_puntajes = ttk.Label(pantalla_puntajes, text="")
lista_puntajes.pack(pady=10)

btn_reinicio = ttk.Button(pantalla_puntajes, command=reiniciar, text="Reiniciar")
btn_reinicio.pack(pady=40)

mostrarPregunta()

if __name__ == "__main__":
    ventana.mainloop()