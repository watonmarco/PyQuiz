import customtkinter as ctk
from preguntas import DATA
import json

class Pregunta:
    def __init__(self, dict_pregunta):
        self.enunciado = dict_pregunta["Pregunta"]
        self.respuestas = dict_pregunta["Opciones"]
        self.respuesta_correcta = dict_pregunta["Respuesta"]

    def getEnunciado(self):
        return self.enunciado
    
    def getOpciones(self):
        return self.respuestas
    
    def getRespuesta(self):
        return self.respuesta_correcta

    def verificarRespuesta(self, respuesta):
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

    enunciado.configure(text=pregunta_actual.getEnunciado())
    botones_opciones.clear()

    for opcion in pregunta_actual.getOpciones():
        if pregunta_actual.verificarRespuesta(opcion):
            boton = ctk.CTkButton(pantalla_quiz, command=responderCorrecto, text=opcion)
        else:
            boton = ctk.CTkButton(pantalla_quiz, command=responderIncorrecto, text=opcion)
        boton.pack(pady=5)
        botones_opciones.append(boton)
    
    btn_siguiente.pack_forget()

def mostrarPregunta():
    puntuacion.place(relx=1, y=0, anchor="ne")
    enunciado.pack(pady=20)
    actualizarInterfaz()

ventana = ctk.CTk()
ventana.title("PyQuiz") 
ventana.geometry('600x450')

# Pantalla de inicio
pantalla_inicio = ctk.CTkFrame(ventana)
pantalla_inicio.pack(fill="both", expand=True)
ctk.CTkLabel(pantalla_inicio, text="Ingrese su nombre:").pack(pady=10)
entrada_nombre = ctk.CTkEntry(pantalla_inicio)
entrada_nombre.pack(pady=10)
btn_iniciar = ctk.CTkButton(pantalla_inicio, text="Iniciar", command=iniciarQuiz)
btn_iniciar.pack(pady=10)

# Pantalla del quiz
pantalla_quiz = ctk.CTkFrame(ventana)

puntuacion = ctk.CTkLabel(pantalla_quiz, text=f"Puntuación: {puntos}")
puntuacion.pack(anchor="ne", padx=10, pady=10)
enunciado = ctk.CTkLabel(pantalla_quiz, text="")
enunciado.pack(pady=20)
resultado = ctk.CTkLabel(pantalla_quiz, text="")
resultado.pack()
btn_siguiente = ctk.CTkButton(pantalla_quiz, command=siguientePregunta, text="Continuar")
botones_opciones = []

# Pantalla de puntajes
pantalla_puntajes = ctk.CTkFrame(ventana)
ctk.CTkLabel(pantalla_puntajes, text="Puntajes:").pack(pady=10)
lista_puntajes = ctk.CTkLabel(pantalla_puntajes, text="")
lista_puntajes.pack(pady=10)

if __name__ == "__main__":
    ventana.mainloop()