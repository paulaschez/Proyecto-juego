import random
import pygame
import constantes

from Jugador import Jugador
from Plataforma import Plataforma
from Puente import Puente
from Utils import guardar
from pantalla_game_over import PantallaGameOver

pygame.init()

# Creacion de pantalla y asignacion de titulo
(alto, ancho) = constantes.TAMANIO_PANTALLA
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption(constantes.NOMBRE_JUEGO)


# Carga de la imagen de fondo y variables relacionadas con su movimiento
imagen_fondo = pygame.image.load(constantes.RUTA_IMG_FONDO)
posicion_fondo = 0
desplazamiento_fondo = False
desplazamiento_actual = 0

# Creacion del jugador
jugador = Jugador()

# Creacion del array de plataformas
plataformas = []
# Variable que controla en qué plataforma se encuentra el jugador
plataforma_index = 0
# Generacion primera plataforma
plataformas.append(Plataforma(0, constantes.POSICION_J_X + jugador.rect.width ))
# Variable para la posicion en el eje x de la plataforma
x_inicial = 0

# Creacion de puente
puente = Puente()
# Variable que calcula la posicion final del puente
pos_final_puente = 0

# Variable para comprobar cuando se ha empezado a mantener pulsado el espacio
# Para que presionar mientras el puente esta cayendo no provoque errores
mantenido = False

pygame.mixer.init()
# Cargar música de fondo
pygame.mixer.music.load(constantes.RUTA_MUSICA_FONDO)
pygame.mixer.music.set_volume(constantes.VOLUMEN_MUSICA)
pygame.mixer.music.play(-1)
mute = False

# Cargar imagenenes icono sonido
img_mute = pygame.transform.scale(pygame.image.load(constantes.RUTA_IMG_MUTE), constantes.TAMANIO_ICONO_SONIDO)
img_unmute = pygame.transform.scale(pygame.image.load(constantes.RUTA_IMG_UNMUTE), constantes.TAMANIO_ICONO_SONIDO)

# Cargar efectos sonoro
sonido_exito = pygame.mixer.Sound(constantes.RUTA_SONIDO_EXITO) # Sonido cuando se alcanza la siguiente platafotma
sonido_caida = pygame.mixer.Sound(constantes.RUTA_SONIDO_CAIDA) # Sonido cuando el jugador se cae
sonido_precision = pygame.mixer.Sound(constantes.RUTA_SONIDO_PERFECTO) # Sonido cuando el puente alcanza la mitad de la siguiente plataforma

# Variable para la puntuacion obtenida
puntuacion = 0

# Variable para la precisión del puente (100 % si alcanza el centro de la plataforma)
precision = 0

# Variable que controla si se ha alcanzado la precision necesaria o no (y mostrar el texto de PERFECTO)
mostrar_perfecto = False

# Fuente para la puntuacion y texto
fuente_puntuacion = pygame.font.Font(constantes.RUTA_FUENTE, 36)
texto_puntuacion = fuente_puntuacion.render(f"Puntuacion: {puntuacion}", True, constantes.NEGRO)

# Variable que controla la posicion de la puntuacion en el eje X
pos_x_puntuacion = 0

# Variable que controla si se debe mostrar el tutorial o no
mostrar_tutorial = True
# Textos y fuentes para el tutorial
fuente_tutorial = pygame.font.Font(constantes.RUTA_FUENTE, 20)
texto_tutorial1 = fuente_tutorial.render(
            "Presiona 'M' para mutear o desmutear la música", True, constantes.NEGRO
        )
texto_tutorial2 = fuente_tutorial.render(
    "Presiona la barra espaciadora para hacer crecer el puente", True, constantes.NEGRO
)
texto_tutorial3 = fuente_tutorial.render(
    "Presiona ENTER para comenzar", True, constantes.NEGRO
)

""" Metodo para dibujar la imagen de fondo. 
    Para el efecto de "infinito" se dibujan dos imagenes una detras de otra.
"""
def dibujar_fondo():
    pantalla.blit(imagen_fondo, (posicion_fondo, 0))
    pantalla.blit(imagen_fondo, (posicion_fondo + pantalla.get_width(), 0))

# Metodo para dibujar las plataformas
def dibujar_plataformas():
    # Recorre el array de plataformas y las dibuja
    for plataforma_ in plataformas:
        plataforma_.draw(pantalla)

""" Metodo para dibujar la puntuacion. 
    Recibe como parametro la posicion en el eje X de debe alcanzar. 
"""
def dibujar_puntuacion(destino_x):

    global pos_x_puntuacion, texto_puntuacion
    texto_puntuacion = fuente_puntuacion.render(f"Puntuacion: {puntuacion}", True, constantes.NEGRO)

    # Si esta jugando la posicion x es igual al destino
    if  jugando:
        pos_x_puntuacion = destino_x
    # Si no esta jugando, se va a desplazar desde su pos inicial al centro de la pantalla
    else:
        if pos_x_puntuacion < destino_x:
            pos_x_puntuacion += constantes.VELOCIDAD_DESPLAZAMIENTO_PANTALLA * 2
    pantalla.blit(texto_puntuacion, (pos_x_puntuacion, 40))

# Metodo para desplazar el fondo cuando el jugador se esta moviendo
def desplazar_fondo():
    global posicion_fondo
    if jugador.moviendose:
        posicion_fondo -= 0.5
    dibujar_fondo()

    # Si la imagen se sale de la pantalla por la izquierda se reinicia a 0 su posicion
    if posicion_fondo <= -pantalla.get_width():
        posicion_fondo = 0

# Metodo para gestionar las plataformas.
def gestionar_plataformas():
    # Mientras el array tenga menos de 5 plataformas, se añaden
    while len(plataformas) < 5:
        nueva_x = plataformas[-1].rect.right + random.randint(50, 200)
        plataformas.append(next(generar_plataforma(nueva_x)))

    # Se elimina la primera plataforma si está fuera de la parte visible de la pantalla
    if plataformas[0].rect.right < 0:
        plataformas.pop(0)
        global plataforma_index
        plataforma_index -= 1

""" Generador de plataformas. 
    Recibe como parametro la posicion en el eje X donde se va a dibujar.
    En funcion de la puntuacion alcanzada, serán cada vez más estrechas.
"""
def generar_plataforma(x_pos):
    global puntuacion

    ancho_max = 200
    ancho_min = jugador.rect.width
    if puntuacion > 10:
        ancho_max = 150
    elif puntuacion > 30:
        ancho_max = 100
    elif puntuacion > 50:
        ancho_max = 75
    while True:
        ancho_plat = random.randint(ancho_min, ancho_max) # Se genera el ancho de forma aleatoria.
        yield Plataforma(x_pos, ancho_plat)

""" Generador de espacios entre las plataformas. 
"""
def generar_espacio():
    while True:
        yield plataformas[-1].rect.width + random.randint(75, 200)


#Inicializacion de plataformas#

for _ in range(5): # Se añaden 5 plataformas
    x_inicial += next(generar_espacio()) # Se obtiene la pos x de la plataforma
    plataformas.append(next(generar_plataforma(x_inicial))) # Se añade la plataforma obtenida a partir de los generadores


# Metodo que verifica que el puente haya alcanzado la siguiente plataforma y no la supere
def verificar_alcance_puente():
    global pos_final_puente
    pos_final_puente = plataformas[plataforma_index].rect.right + puente.longitud - puente.puente_completo_width
    siguiente_plataforma = plataformas[plataforma_index + 1]

    return siguiente_plataforma.rect.left <= pos_final_puente <= siguiente_plataforma.rect.right

# Metodo que reinicia todos las variables a los valores del inicio cuando se comienza de nuevo
def reiniciar_juego():
    global jugador, puente, plataformas, plataforma_index, puntuacion, jugando, desplazamiento_actual, mute, x_inicial
    mute = False
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    plataformas.clear()
    plataformas.append(Plataforma(0, constantes.POSICION_J_X + jugador.rect.width))
    plataforma_index = 0

    x_inicial = 0
    jugador = Jugador()
    puente = Puente()
    puntuacion = 0
    for _ in range(5):
        x_inicial += next(generar_espacio())
        plataformas.append(next(generar_plataforma(x_inicial)))
    jugando = True
    desplazamiento_actual = 0
    jugador.posicion_jugador_y = constantes.POSICION_J_Y



# Bucle del juego
running = True
jugando = True  # Variable para saber si estamos jugando o en la pantalla de Game Over
pantalla_game_over = PantallaGameOver()  # Crear instancia de la pantalla de Game Over

while running:
    # Manejo de enventos
    for event in pygame.event.get():
        # Si el jugador cierra el juego se termina el bucle, y el juego
        if event.type == pygame.QUIT:
            running = False

        # Si se esta mostrando el tutorial y se hace clic en ENTER se quita
        if mostrar_tutorial and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                mostrar_tutorial = False

        # Si se presiona M se mutea al juego
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if mute:
                    mute = False
                    pygame.mixer.music.set_volume(constantes.VOLUMEN_MUSICA)

                else:
                    mute = True
                    pygame.mixer.music.set_volume(0)

        # Si no se está mostrando el tutorial, se gestionan los eventos del funcionamiento del juego
        if not mostrar_tutorial:

            # Si el juego ha terminado
            if not jugando:
                resultado = pantalla_game_over.manejar_eventos(event) # Segun a  que tecla le de devuelve la cadena
                if resultado == "reiniciar":
                    reiniciar_juego() # Si presiona M se reinicia el juego

                elif resultado == "salir":
                    running = False  # Si presiona Escape se termina el juego

            # Si se esta jugando y el dinosaurio no esta en movimiento
            elif not jugador.moviendose:
                # Si el jugador mantiene presionada la barra espaciadora (solo cuando esta quieto el dinosaurio)
                # crece el puente
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not puente.caido and not puente.cayendo:
                        puente.creciendo = True
                        mantenido = True
                elif event.type == pygame.KEYUP and mantenido:
                    if event.key == pygame.K_SPACE:
                        puente.creciendo = False
                        puente.cayendo = True
                        mantenido = False




    if jugando:
        pantalla_game_over.reiniciar() # Se reinicia los valores de la pantalla de gameover al comenzar a jugar
        jugador.actualizar_animacion() # Actualiza la animacion
        puente.actualizar(puntuacion) # Actualiza la velovidad de crecimiento del fuente

        # Si el puente ha terminado de caer
        if puente.caido:
            puente.caido = False
            jugador.moviendose = True # El jugador comenzara a "moverse"
            jugador.cambiar_animacion("caminando") # Se cambia la animacion

        # Mientras el jugador se mueve
        if jugador.moviendose:
            # Antes de comenzar a moverse
            if desplazamiento_actual == 0:
                # Si el puente ha alcanzado la siguiente plataforma
                if verificar_alcance_puente():

                    # Se calcula la distancia que el jugador debe recorrer para llegar a la siguiente plataforma
                    desplazamiento_objetivo = plataformas[plataforma_index + 1].rect.left - jugador.posicion_jugador_x

                    #  Calculo de la precision en base a qué tan cerca cayo el puente del centro de la plataforma
                    distancia = abs(pos_final_puente - plataformas[plataforma_index + 1].rect.centerx)
                    precision = max(0, 100 - distancia)  # Cuanto más cerca del centro, mejor precisión

                # Si el puente no alcanza la plataforma
                else:
                    # Se calcula la distancia que el jugador debe recorrer hasta caer al vacio
                    desplazamiento_objetivo = puente.longitud + jugador.rect.width

            # Si no se ha llegado al objetivo ( mientras se esta moviendo)
            if desplazamiento_actual < desplazamiento_objetivo:
                # Se desplazan las plataformas gradualmente hasta que llega al objetivo
                for plataforma in plataformas:
                    plataforma.actualizar()
                desplazamiento_actual += constantes.VELOCIDAD_DESPLAZAMIENTO_PANTALLA

                # Si la precision es entre 95 / 100 se mostrara el texto y se reproduce el sonido
                if precision >= 95:
                    mostrar_perfecto = True
                    sonido_precision.play()
            # Cuando se ha alcanzado el objetivo
            else:
                # Si el puente alcanza la plat
                if verificar_alcance_puente():

                    # En función de la precisión
                    if precision >= 95:
                        puntuacion += 2 # Se incrementa el doble la puntuacion
                        mostrar_perfecto = False  # Se deja de mostrar el texto de perfecto

                    else:
                        sonido_exito.play() # Se reproduce el sonido de exito
                        puntuacion += 1 # Se incremente en uno la puntuacion

                    # Reasignacion valores para el siguiente ciclo
                    precision = 0 # Reinicia la precision
                    plataforma_index += 1  # Se aumenta el índice de la plataforma
                    desplazamiento_actual = 0  # Reinicia el desplazamiento
                    jugador.moviendose = False  # Deja de mover al jugador
                    jugador.cambiar_animacion("reposo")  # Cambia a la animación a reposo
                    puente.reiniciar()  # Reinicia la longitud del puente

                # Si no alcanza la plataforma
                else:
                    pygame.mixer.music.stop()  # Se detiene la música de fondo
                    sonido_caida.play() # Se reproduce el sonido de caida
                    jugador.cambiar_animacion("muerte")  # Cambia a la animación a muerte
                    # El jugador cae al vacio
                    jugador.posicion_jugador_y += constantes.VELOCIDAD_DESPLAZAMIENTO_PANTALLA
                    jugador.actualizar_animacion()

                   # Una vez que el jugador desaparece de la pantalla
                    if jugador.posicion_jugador_y >= jugador.rect.height + alto:
                        guardar(puntuacion) # Se guarda la puntuacion
                        jugando = False # Se termina la partida


        # Se añaden o se eliminan plataformas del array
        gestionar_plataformas()


        # Dibujado de elementos
        desplazar_fondo()
        dibujar_plataformas()
        dibujar_puntuacion(constantes.POS_X_PUNTUACION)

        # Dibuja el texto en la pantalla
        if mostrar_perfecto:
            texto_precision = fuente_puntuacion.render("PERFECTO", True, constantes.NEGRO)
            pantalla.blit(texto_precision, (plataformas[plataforma_index+1].rect.x, 300))


        # Dibuja los iconos de sonido en funcion de si esta en mute o no
        if mute:
            pantalla.blit(img_mute, (ancho - (img_mute.get_width()*1.25) ,40))
        else:
            pantalla.blit(img_unmute, (ancho - (img_unmute.get_width()*1.25),40))

        # Dibuja los textos del tutorial
        if mostrar_tutorial:
            pantalla.blit(texto_tutorial1, (ancho / 2 - texto_tutorial1.get_width() / 2, alto / 3))
            pantalla.blit(texto_tutorial2, (ancho / 2 - texto_tutorial2.get_width() / 2, alto / 3 + 40))
            pantalla.blit(texto_tutorial3, (ancho / 2 - texto_tutorial3.get_width() / 2, alto / 3 + 80))

        # Dibujado de jugador
        jugador.draw(pantalla)

        # Dibujado de puente
        puente.dibujar(pantalla, plataformas[plataforma_index].rect)


    # Si no se ha perdido
    else:

        dibujar_fondo() # Dibuja la pantalla
        jugador.draw(pantalla) # Dibuja al jugador
        dibujar_puntuacion(constantes.ANCHO_PANTALLA / 2 - texto_puntuacion.get_width() / 2) # El texto se mueve hasta alcanzar el centro
        dibujar_plataformas() # Se dibujan las pantallas

        pantalla_game_over.actualizar() # Actualiza la posicion del cartel para que 'caiga'
        pantalla_game_over.mostrar(pantalla) # Muestra la pantalla de game oven

    pygame.display.flip() # Actualiza la pantalla despues de cada frame
    pygame.time.Clock().tick(60) # Mantiene el juego a 60fps

pygame.quit() # Detiene pygame

