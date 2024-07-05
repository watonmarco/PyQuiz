import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
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
        return self.respuestas.index(respuesta) == self.getRespuesta()

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntos = 0
        self.vidas = 3

    def getNombre(self):
        return self.nombre

    def getPuntos(self):
        return self.puntos
    
    def setPuntos(self, nueva_puntacion):
        self.puntos = nueva_puntacion

    def sumarPuntos(self):
        self.puntos += 1
    
    def getVidas(self):
        return self.vidas
    
    def setVidas(self, num_vidas):
        self.vidas = num_vidas

    def restarVidas(self):
        global corazones
        self.vidas -= 1
        corazones[-1].config(image="")
        corazones.pop()


class InterfazJSON:
    def __init__(self):
        self.preguntas = DATA

    def guardarPuntaje(self, nombre, puntos):
        puntajes = self.cargarPuntajes()
        puntajes.append({"nombre": nombre, "puntaje": puntos})
        with open("puntajes.json", "w") as file: # "w" = write
            json.dump(puntajes, file) # para escribir sobre el .json

    def cargarPuntajes(self):
        try:
            with open("puntajes.json", "r") as file: # "r" = read
                return json.load(file) # se carga el contenido del .json y lo muestra
        except FileNotFoundError:
            return []
    
    def getPreguntas(self):
        return self.preguntas

    def borrarPuntajes(self):
        with open('puntajes.json', 'r') as file:
            data = json.load(file)
        
        # checking if the key exists before removing
        for key_to_remove in data:
            data.pop(key_to_remove)
        
        # saving the updated JSON data back to the file
        with open('output.json', 'w') as file:
            json.dump(data, file, indent=2)


js = InterfazJSON()
preguntas_ronda = js.getPreguntas().copy()

temp_pregunta = rd.choice(preguntas_ronda)
pregunta_actual = Pregunta(temp_pregunta)

def iniciarQuiz():

    global jgd
    jgd = Jugador(entrada_nombre.get())

    if (jgd.getNombre() != "admin") and (jgd.getNombre() != ""):
        pantalla_inicio.pack_forget()
        pantalla_quiz.pack(fill="both")
        mostrarPregunta()
        mostrarJugador()
        mostrarVidas()
        jgd.setPuntos(0)
        jgd.setVidas(3)
        puntuacion.configure(text=f"Puntuación: {jgd.getPuntos()}")

    elif jgd.getNombre() == "admin":
        btn_iniciar.state(["disabled"])
        btn_admin = ttk.Button(pantalla_inicio, command=mostrarPuntajesAdmin, text="admin")
        btn_admin.pack(pady=10)


def jugar():
    pantalla_principal.pack_forget()
    pantalla_inicio.pack(fill="both", expand=True)

def mostrarPuntajes():
    pantalla_quiz.pack_forget()
    pantalla_principal.pack_forget()
    pantalla_puntajes.pack(fill="both", expand=True)

    puntajes = js.cargarPuntajes()
    puntajes_ordenados = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)[:10] # se ordenan los 10 mejores puntajes de forma descendente
    texto_puntajes = "\n".join([f"{i+1}. {p['nombre']}: {p['puntaje']}" for i, p in enumerate(puntajes_ordenados)]) # se muestran los puntajes enumerados
    lista_puntajes.configure(text=texto_puntajes)

def mostrarPuntajesAdmin():
    mostrarPuntajes()
    btn_borrar = btn_volver = ttk.Button(pantalla_puntajes, command=borrar, text="Volver")
    btn_borrar.pack(anchor="ne", padx=10, pady=30)

def responderCorrecto():
    resultado.configure(text="¡Correcto!")
    resultado.pack()
    btn_siguiente.pack(pady=30)
    desactivarBotones()

    global jgd
    jgd.sumarPuntos() 
    puntuacion.configure(text=f"Puntuación: {jgd.getPuntos()}")
    
def responderIncorrecto():
    resultado.configure(text="Incorrecto")
    resultado.pack()
    btn_siguiente.pack(pady=30)
    desactivarBotones()

    global jgd
    jgd.restarVidas()

def desactivarBotones():
    for boton in botones_opciones:
        boton.state(['disabled']) # se cambia el estado del botón a "desactivado"

def terminarJuego():
    global corazones, js
    js.guardarPuntaje(jgd.getNombre(), jgd.getPuntos())
    mostrarPuntajes()
    for corazon in corazones:
        corazon.config(image="")

def siguientePregunta():
    global preguntas_ronda, pregunta_actual, temp_pregunta
    
    if jgd.getVidas() <= 0:
        terminarJuego()

    if temp_pregunta in preguntas_ronda:
        preguntas_ronda.remove(temp_pregunta)
        
    if len(preguntas_ronda) != 0:
        temp_pregunta = rd.choice(preguntas_ronda)
        pregunta_actual = Pregunta(temp_pregunta)
        actualizarInterfaz()
    else:
        terminarJuego()

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
    enunciado.pack(pady=30)

    actualizarInterfaz()
    
def reiniciar():
    global pregunta_actual, jgd, preguntas_ronda, temp_pregunta

    preguntas_ronda = DATA.copy()
    temp_pregunta = rd.choice(preguntas_ronda)
    pregunta_actual = Pregunta(temp_pregunta)

    #jgd.setPuntos(0) # movido a función jugar()
    #jgd.setVidas(3)  # movido a función jugar()
    
    #puntuacion.configure(text=f"Puntuación: {jgd.getPuntos()}") # movido a función jugar()
    actualizarInterfaz()
    
    pantalla_quiz.pack_forget()
    pantalla_puntajes.pack_forget()
    pantalla_principal.pack(fill="both")

def volver():
    reiniciar()
    for corazon in corazones:
        corazon.config(image="")

def borrar():
    if jgd.getNombre == "admin":
        js.borrarPuntajes()
        

def mostrarJugador():
    jugador = ttk.Label(pantalla_quiz, text=f"Jugador: {jgd.getNombre()}")
    jugador.place(x=10, y=10, anchor="nw")

def mostrarVidas():
    global corazones
    vidastxt = ttk.Label(pantalla_quiz, text="Vidas: ")
    vidastxt.place(x=10, y=31, anchor="nw")
    espaciado = 45
    corazones = []
    for i in range(jgd.getVidas()):
        corazon = tk.Label(ventana, image=img_vidas)
        corazon.place(x=espaciado, y=33, anchor="nw")
        espaciado += 20
        corazones.append(corazon)
            
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
puntuacion = ttk.Label(pantalla_quiz, text=f"Puntuación: {0}")
puntuacion.pack(anchor="ne", padx=10, pady=10)

btn_volver = ttk.Button(pantalla_quiz, command=volver, text="Volver")
btn_volver.pack(anchor="ne", padx=10, pady=30)

enunciado = ttk.Label(pantalla_quiz, text="")
resultado = ttk.Label(pantalla_quiz, text="")
btn_siguiente = ttk.Button(pantalla_quiz, command=siguientePregunta, text="Continuar")
botones_opciones = []

img_vidas = PhotoImage(file="HeartSprite (3).png")

#btn_salir = ttk.Button(pantalla_quiz, text="Salir", command=iniciarQuiz)
#btn_salir.pack()

# Pantalla de puntajes
pantalla_puntajes = ttk.Frame(ventana)
ttk.Label(pantalla_puntajes, text="Puntajes:").pack(pady=10)
lista_puntajes = ttk.Label(pantalla_puntajes, text="")
lista_puntajes.pack(pady=10)

btn_reinicio = ttk.Button(pantalla_puntajes, command=reiniciar, text="Volver")
btn_reinicio.pack(pady=40)

mostrarPregunta()

if __name__ == "__main__":
    ventana.mainloop()