import cv2
from gtts import gTTS
import os
import pygame
import time

def detect_and_recognize_faces():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Video', frame)

        if len(faces) > 0:
            text_to_speech_and_animate("Hola, bienvenido a la Fundación Clínica Noel. Es un placer tenerte aquí. A continuación, por favor ingresa el número de documento del paciente y haz clic en el botón OK. Luego, ingresa el número de celular y dirígete a Admisiones.")
            break  # Salimos del bucle después de detectar una cara

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def text_to_speech_and_animate(text):
    words = text.split()
    word_timings = assign_timings_to_words(words)

    tts = gTTS(text=text, lang='es')
    tts.save("output.mp3")
    os.system("start output.mp3")  # Cambia a "mpg321 output.mp3" en Linux

    animar_muñeco_con_texto(words, word_timings)

def assign_timings_to_words(words):
    # Aquí puedes implementar lógica para asignar tiempos a las palabras
    # Por ahora, asignaremos a cada palabra un tiempo de 1 segundo
    return [1] * len(words)

def animar_muñeco_con_texto(palabras, tiempos):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Muñeco Signando')

    tiempo_inicial = time.time()
    indice_palabra = 0

    while indice_palabra < len(palabras):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        palabra_actual = palabras[indice_palabra]
        tiempo_asignado = tiempos[indice_palabra]

        movimiento = asignar_movimientos_a_palabras([palabra_actual])[0]
        
        if movimiento == 'saludo':
            draw_character(screen, waving=True)
        elif movimiento == 'despedida':
            draw_character(screen, waving=False)
        else:
            draw_character(screen, waving=False)

        tiempo_transcurrido = time.time() - tiempo_inicial
        if tiempo_transcurrido >= tiempo_asignado:
            indice_palabra += 1
            tiempo_inicial = time.time()

        pygame.display.flip()  # Actualizar la ventana

    pygame.quit()

def draw_character(screen, waving=False):
    # Dibujar el personaje utilizando formas básicas
    pygame.draw.circle(screen, (255, 0, 0), (400, 300), 50)  # Cabeza
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(375, 350, 50, 100))  # Cuerpo
    pygame.draw.line(screen, (0, 0, 255), (375, 350), (325, 250), 5)  # Brazo izquierdo
    pygame.draw.line(screen, (0, 0, 255), (425, 350), (475, 250), 5)  # Brazo derecho
    pygame.draw.line(screen, (0, 0, 255), (400, 450), (375, 550), 5)  # Pierna izquierda
    pygame.draw.line(screen, (0, 0, 255), (400, 450), (425, 550), 5)  # Pierna derecha
    
    if waving:
        # Aquí puedes agregar lógica para animar el muñeco saludando
        # Por ejemplo, levantar la mano o hacer un gesto de saludo con la cabeza
        pass

def asignar_movimientos_a_palabras(palabras):
    movimientos = []
    
    for palabra in palabras:
        if palabra.lower() == 'hola':
            movimientos.append('saludo')
        elif palabra.lower() == 'adiós':
            movimientos.append('despedida')
        else:
            movimientos.append('reposo')  # Por defecto, no hay movimiento
    return movimientos

detect_and_recognize_faces()
