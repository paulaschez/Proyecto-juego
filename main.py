import random
import pygame
import constantes

from Jugador import Jugador
from Plataforma import Plataforma
from Puente import Puente

pygame.init()

(alto, ancho) = constantes.TAMANIO_PANTALLA

pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("DinoDash")

imagen_fondo = pygame.image.load(constantes.RUTA_IMG_FONDO)
posicion_fondo = 0
desplazamiento_fondo = False
desplazamiento_actual = 0

plataformas = []
plataforma_index = 0

mantenido = False

jugador = Jugador()
puente = Puente()

# Generacion primera plataforma
plataformas.append(Plataforma(0, ancho / 2 + jugador.rect.width * 2 ))


def generar_plataforma(x_pos):
    while True:
        ancho_plat = random.randint(50, 150)
        yield Plataforma(x_pos, ancho_plat)

def generar_espacio(index = -1):
    while True:
        yield plataformas[index].rect.width + random.randint(100, 200)

# Inicializacion de plataformas
x_inicial = next(generar_espacio(0))

for _ in range(5): # Se comienza añadiendo 5 plataformas
    plataformas.append(next(generar_plataforma(x_inicial)))
    x_inicial += next(generar_espacio())

# Verifica que el puente haya alcanzado la siguiente plataforma y no la supere
def verificar_alcance_puente():
    pos_final_puente = plataformas[plataforma_index].rect.right + puente.longitud
    siguiente_plataforma = plataformas[plataforma_index + 1]

    return siguiente_plataforma.rect.left <= pos_final_puente <= siguiente_plataforma.rect.right

# Bucle del juego
running = True

while running:
    # Manejo de enventos
    for event in pygame.event.get():
        # Si el jugador cierra el juego se termina el bucle, y el juego
        if event.type == pygame.QUIT:
            running = False
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

    jugador.actualizar_animacion()
    puente.actualizar()

    if puente.caido:
        puente.caido = False

        if verificar_alcance_puente():
            jugador.moviendose = True
            jugador.cambiar_animacion("caminando")
        else:
            print("¡Has caído! Intenta de nuevo.")
            running = False  # Termina el juego"""

    # Mientras el jugador se mueve
    if jugador.moviendose:
        # Se desplaza el fondo
        posicion_fondo -= 0.5


        # Se calcula el desplazamiento objetivo cuando comienza el movimiento
        if desplazamiento_actual == 0:
            desplazamiento_objetivo = plataformas[plataforma_index + 1].rect.left - jugador.posicion_jugador_x

        # Se desplazan las plataformas gradualmente hasta que llega al objetivo
        if desplazamiento_actual < desplazamiento_objetivo:
            for plataforma in plataformas:
                plataforma.rect.x -= constantes.VELOCIDAD_DESPLAZAMIENTO_PANTALLA
            desplazamiento_actual += constantes.VELOCIDAD_DESPLAZAMIENTO_PANTALLA
        else:
            # Si el desplazamiento se completó, alinea el jugador y reinicia

            plataforma_index += 1 # Se aumenta el indice de la plataforma en la que se encuentra
            desplazamiento_actual = 0  # Reinicia el desplazamiento
            jugador.moviendose = False  # Deja de mover al jugador
            jugador.cambiar_animacion("reposo") # Cambia la animacion por la de reposo
            puente.reiniciar()  # Reinicia la longitud del puente


    # Mientras que las plataformas que estan en el array sea menor que cinco, seguira añadadiendo una al final
    while len(plataformas) < 5:
        # Generar nueva plataforma al final
        nueva_x = plataformas[-1].rect.right + random.randint(100, 200)
        plataformas.append(next(generar_plataforma(nueva_x)))

    # Eliminar las plataformas de la izquierda que se salgan de la pantalla
    if plataformas[0].rect.right < 0:
        plataformas.pop(0)
        plataforma_index -= 1


    # Dibujado de pantalla
    pantalla.blit(imagen_fondo, (posicion_fondo, 0))
    pantalla.blit(imagen_fondo, (posicion_fondo + pantalla.get_width(), 0))

    if posicion_fondo <= -pantalla.get_width():
        posicion_fondo = 0


    # Dibujado de plataformas
    for plataforma in plataformas:
        plataforma.draw(pantalla)

    # Dibujado de jugador
    jugador.draw(pantalla)

    # Dibujado de puente
    puente.dibujar(pantalla, plataformas[plataforma_index].rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

