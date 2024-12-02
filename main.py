import random
import pygame
import constantes

from Jugador import Jugador
from Plataforma import Plataforma
from Puente import Puente
from Utils import guardar
from pantalla_game_over import PantallaGameOver

pygame.init()

(alto, ancho) = constantes.TAMANIO_PANTALLA

pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("DinoDash")

imagen_fondo = pygame.image.load(constantes.RUTA_IMG_FONDO)
posicion_fondo = 0
desplazamiento_fondo = False
desplazamiento_actual = 0


jugador = Jugador()

plataformas = []
plataforma_index = 0
# Generacion primera plataforma
plataformas.append(Plataforma(0, constantes.POSICION_J_X + jugador.rect.width ))


puente = Puente()
pos_final_puente = 0
mantenido = False

pygame.mixer.init()
# Cargar música de fondo
pygame.mixer.music.load("media/musica/musica_fondo.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
mute = False

img_mute = pygame.transform.scale(pygame.image.load("media/graficos/pantalla_principal/mute.png"), (50, 35))
img_unmute = pygame.transform.scale(pygame.image.load("media/graficos/pantalla_principal/unmute.png"), (50, 35))

# Cargar efecto sonoro
sonido_exito = pygame.mixer.Sound("media/musica/exito.mp3")
sonido_caida = pygame.mixer.Sound("media/musica/game_over.mp3")
sonido_precision = pygame.mixer.Sound("media/musica/precision.mp3")

puntuacion = 0
precision = 0
mostrar_perfecto = False
fuente_puntuacion = pygame.font.Font(constantes.RUTA_FUENTE, 36)
texto_puntuacion = fuente_puntuacion.render(f"Puntuacion: {puntuacion}", True, (0, 0, 0))

pos_puntuacion = 0

mostrar_tutorial = True
fuente_tutorial = pygame.font.Font(constantes.RUTA_FUENTE, 20)
texto_tutorial1 = fuente_tutorial.render(
            "Presiona 'M' para mutear o desmutear la música", True, (0, 0, 0)
        )
texto_tutorial2 = fuente_tutorial.render(
    "Presiona la barra espaciadora para hacer crecer el puente", True, (0, 0, 0)
)
texto_tutorial3 = fuente_tutorial.render(
    "Presiona ENTER para comenzar", True, (0, 0, 0)
)

def dibujar_fondo():
    pantalla.blit(imagen_fondo, (posicion_fondo, 0))
    pantalla.blit(imagen_fondo, (posicion_fondo + pantalla.get_width(), 0))

def dibujar_plataformas():
    # Dibujado de plataformas
    for plataforma_ in plataformas:
        plataforma_.draw(pantalla)

def dibujar_puntuacion(destino_x):

    global pos_puntuacion, texto_puntuacion
    texto_puntuacion = fuente_puntuacion.render(f"Puntuacion: {puntuacion}", True, (0, 0, 0))
    if  jugando:
        pos_puntuacion = destino_x
    else:
        if pos_puntuacion < destino_x:
            pos_puntuacion += constantes.VELOCIDAD_DESPLAZAMIENTO_PANTALLA*2

    pantalla.blit(texto_puntuacion, (pos_puntuacion, 40))


def desplazar_fondo():
    global posicion_fondo
    if jugador.moviendose:
        posicion_fondo -= 0.5
    dibujar_fondo()

    if posicion_fondo <= -pantalla.get_width():
        posicion_fondo = 0

def gestionar_plataformas():
    # Añadir nuevas plataformas si hay menos de 5
    while len(plataformas) < 5:

        nueva_x = plataformas[-1].rect.right + random.randint(50, 200)
        plataformas.append(next(generar_plataforma(nueva_x)))

    # Eliminar plataformas fuera de la pantalla
    if plataformas[0].rect.right < 0:
        plataformas.pop(0)
        global plataforma_index
        plataforma_index -= 1

def generar_plataforma(x_pos):

    ancho_max = 200
    ancho_min = jugador.rect.width
    if puntuacion > 10:
        ancho_max = 150
    elif puntuacion > 30:
        ancho_max = 100
    elif puntuacion > 50:
        ancho_max = 75
    while True:
        ancho_plat = random.randint(ancho_min, ancho_max)
        yield Plataforma(x_pos, ancho_plat)

def generar_espacio(index = -1):
    while True:
        yield plataformas[index].rect.width + random.randint(75, 200)

# Inicializacion de plataformas
x_inicial = next(generar_espacio(0))

for _ in range(5): # Se comienza añadiendo 5 plataformas
    plataformas.append(next(generar_plataforma(x_inicial)))
    x_inicial += next(generar_espacio())

# Verifica que el puente haya alcanzado la siguiente plataforma y no la supere
def verificar_alcance_puente():
    global pos_final_puente
    pos_final_puente = plataformas[plataforma_index].rect.right + puente.longitud - puente.puente_completo_width
    siguiente_plataforma = plataformas[plataforma_index + 1]

    return siguiente_plataforma.rect.left <= pos_final_puente <= siguiente_plataforma.rect.right

def reiniciar_juego():
    global jugador, puente, plataformas, plataforma_index, puntuacion, jugando, desplazamiento_actual, mute
    mute = False
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    plataformas.clear()
    plataformas.append(Plataforma(0, constantes.POSICION_J_X + jugador.rect.width))
    plataforma_index = 0

    jugador = Jugador()
    puente = Puente()
    puntuacion = 0
    pos_x_plataforma = next(generar_espacio(0))
    for _ in range(5):
        plataformas.append(next(generar_plataforma(pos_x_plataforma)))
        pos_x_plataforma += next(generar_espacio())
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

        if mostrar_tutorial and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                mostrar_tutorial = False

        if not mostrar_tutorial:
            # Para silenciar o reproducir la musica
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if mute:
                        mute = False
                        pygame.mixer.music.set_volume(0.2)

                    else:
                        mute= True
                        pygame.mixer.music.set_volume(0)
            # Si el juego ha terminado y se muestra la pantalla de GameOver
            if not jugando:
                resultado = pantalla_game_over.manejar_eventos(event)
                if resultado == 'reiniciar':
                    reiniciar_juego()

                elif resultado == 'salir':
                    running = False  # Si presionas Escape, sale del juego

            # Si el dinosaurio no esta en movimiento
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
        pantalla_game_over.reiniciar()
        jugador.actualizar_animacion()
        puente.actualizar(puntuacion)

        if puente.caido:
            puente.caido = False
            jugador.moviendose = True
            jugador.cambiar_animacion("caminando")

        # Mientras el jugador se mueve
        if jugador.moviendose:
            if desplazamiento_actual == 0:
                if verificar_alcance_puente():
                    desplazamiento_objetivo = plataformas[plataforma_index + 1].rect.left - jugador.posicion_jugador_x

                    distancia = abs(pos_final_puente - plataformas[plataforma_index + 1].rect.centerx)
                    precision = max(0, 100 - distancia)  # Cuanto más cerca del centro, mejor precisión

                else:
                    desplazamiento_objetivo = puente.longitud + jugador.rect.width

            # Se desplazan las plataformas gradualmente hasta que llega al objetivo
            if desplazamiento_actual < desplazamiento_objetivo:
                for plataforma in plataformas:
                    plataforma.actualizar()
                desplazamiento_actual += constantes.VELOCIDAD_DESPLAZAMIENTO_PANTALLA

                # Dibujar la puntuación
                if precision >= 95:
                    mostrar_perfecto = True
                    sonido_precision.play()

            else:
                if verificar_alcance_puente():
                    mostrar_perfecto = False

                    # Acciones al alcanzar la siguiente plataforma
                    if precision >= 95:
                        puntuacion += 2
                    else:
                        sonido_exito.play()
                        puntuacion += 1

                    precision = 0
                    plataforma_index += 1  # Se aumenta el índice de la plataforma
                    desplazamiento_actual = 0  # Reinicia el desplazamiento
                    jugador.moviendose = False  # Deja de mover al jugador
                    jugador.cambiar_animacion("reposo")  # Cambia a la animación de reposo
                    puente.reiniciar()  # Reinicia la longitud del puente
                else:
                    pygame.mixer.music.stop()  # Detener la música de fondo

                    sonido_caida.play()
                    # Acciones al fallar
                    jugador.cambiar_animacion("muerte")
                    jugador.posicion_jugador_y += constantes.VELOCIDAD_DESPLAZAMIENTO_PANTALLA
                    jugador.actualizar_animacion()
                    if jugador.posicion_jugador_y >= jugador.rect.height + alto:
                        guardar(puntuacion)
                        jugando = False



        gestionar_plataformas()


        # Dibujado de pantalla
        desplazar_fondo()

        dibujar_plataformas()

        dibujar_puntuacion(10)

        if mostrar_perfecto:
            texto_precision = fuente_puntuacion.render("PERFECTO", True, (0, 0, 0))
            pantalla.blit(texto_precision, (plataformas[plataforma_index+1].rect.x, 300))



        if mute:
            pantalla.blit(img_mute, (ancho - (img_mute.get_width()*1.25) ,40))
        else:
            pantalla.blit(img_unmute, (ancho - (img_unmute.get_width()*1.25),40))

        if mostrar_tutorial:
            pantalla.blit(texto_tutorial1, (ancho / 2 - texto_tutorial1.get_width() / 2, alto / 3))
            pantalla.blit(texto_tutorial2, (ancho / 2 - texto_tutorial2.get_width() / 2, alto / 3 + 40))
            pantalla.blit(texto_tutorial3, (ancho / 2 - texto_tutorial3.get_width() / 2, alto / 3 + 80))

        # Dibujado de jugador
        jugador.draw(pantalla)

        # Dibujado de puente
        puente.dibujar(pantalla, plataformas[plataforma_index].rect)

        pygame.display.flip()
    else:

        dibujar_fondo()
        jugador.draw(pantalla)
        dibujar_puntuacion(constantes.ANCHO_PANTALLA / 2 - texto_puntuacion.get_width() / 2)
        dibujar_plataformas()

        pantalla_game_over.actualizar()
        pantalla_game_over.mostrar(pantalla)
        pygame.display.flip()  # Actualiza la pantalla
    pygame.time.Clock().tick(60)

pygame.quit()

