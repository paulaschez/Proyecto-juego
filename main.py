import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Puentes")

# Colores
COLOR_FONDO = (135, 206, 235)  # Azul cielo
COLOR_PLATAFORMA = (100, 100, 100)  # Gris oscuro
COLOR_JUGADOR = (255, 69, 0)  # Naranja
COLOR_PUENTE = (0, 0, 0)  # Negro

# Parámetros del juego
TAMAÑO_JUGADOR = 20
VELOCIDAD_CRECE_PUENTE = 5
VELOCIDAD_DESPLAZAMIENTO_PANTALLA = 5
posicion_jugador_x = 400
posicion_jugador_y = ALTO - 100
IMAGEN_FONDO = pygame.image.load("media/fondo.jpg")
posicion_fondo = 0

# Listas de plataformas y variables del puente
plataformas = []
altura_puente = 0
creciendo_puente = False
puente_caido = False
longitud_puente = 0
moviendo_jugador = False
plataforma_index = 0
desplazamiento_fondo = False
desplazamiento_actual = 0  # Cantidad desplazada hasta ahora

# ancho de la primera plataforma
ancho =  ANCHO / 2 + TAMAÑO_JUGADOR * 2
plataformas.append(pygame.Rect(0, posicion_jugador_y, ancho, 20))

# Generación de plataformas aleatorias
def generar_plataforma(x_pos):
    while True:
        ancho = random.randint(50, 150)
        yield pygame.Rect(x_pos, posicion_jugador_y, ancho, 20)

# Inicialización de plataformas
x_inicial = plataformas[0].width + random.randint(100, 200)
for _ in range(5):  # Comenzamos con 5 plataformas

    plataformas.append(next(generar_plataforma(x_inicial)))
    x_inicial += plataformas[-1].width + random.randint(100, 200)

# Bucle del juego
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not puente_caido:
                creciendo_puente = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                creciendo_puente = False
                puente_caido = True  # El puente cae al soltar la barra

    # Lógica del puente
    if creciendo_puente:
        altura_puente += VELOCIDAD_CRECE_PUENTE
    elif puente_caido:
        longitud_puente = altura_puente  # Guardamos la altura como longitud del puente caído
        altura_puente = 0  # Reiniciamos la altura
        puente_caido = False

        # Verificación del alcance del puente
        posicion_final_puente = plataformas[plataforma_index].right + longitud_puente
        siguiente_plataforma = plataformas[plataforma_index + 1] if plataforma_index + 1 < len(plataformas) else None

        # Comprobamos si el puente cae sobre la siguiente plataforma
        if siguiente_plataforma and siguiente_plataforma.left <= posicion_final_puente <= siguiente_plataforma.right:
            # Éxito: mueve al jugador a la siguiente plataforma
            moviendo_jugador = True
        else:
            # Falla: el jugador cae
            print("¡Has caído! Intenta de nuevo.")
            running = False  # Termina el juego

    # Movimiento del jugador o desplazamiento de plataformas
    if moviendo_jugador:
        # Se calcula el desplazamiento cuando comienza el movimiento
        if desplazamiento_actual == 0:
            desplazamiento_objetivo = plataformas[plataforma_index + 1].left - posicion_jugador_x

        # Desplazar plataformas gradualmente
        if desplazamiento_actual < desplazamiento_objetivo:
            for plataforma in plataformas:
                plataforma.x -= VELOCIDAD_DESPLAZAMIENTO_PANTALLA
            desplazamiento_actual += VELOCIDAD_DESPLAZAMIENTO_PANTALLA
        else:
            # Si el desplazamiento se completó, alinea el jugador y reinicia
            plataforma_index += 1
            desplazamiento_actual = 0  # Reinicia el desplazamiento
            moviendo_jugador = False  # Deja de mover al jugador
            longitud_puente = 0  # Reinicia la longitud del puente



    while len(plataformas) < 5:
        # Generar nueva plataforma al final
        nueva_x = plataformas[-1].right + random.randint(100, 200)
        plataformas.append(next(generar_plataforma(nueva_x)))

    if plataformas[0].right < 0:
        plataformas.pop(0)
        plataforma_index-=1

    # Dibujado de la pantalla
    screen.blit(IMAGEN_FONDO, (posicion_fondo, 0))
    screen.blit(IMAGEN_FONDO,  (posicion_fondo + screen.get_width(), 0))
    if moviendo_jugador:
        posicion_fondo -= 0.5

    if posicion_fondo <= -screen.get_width():
        posicion_fondo = 0


    # Dibujar plataformas
    for plataforma in plataformas:
        pygame.draw.rect(screen, COLOR_PLATAFORMA, plataforma)

    # Dibujar jugador
    pygame.draw.rect(screen, COLOR_JUGADOR,
                     (posicion_jugador_x, posicion_jugador_y - TAMAÑO_JUGADOR, TAMAÑO_JUGADOR, TAMAÑO_JUGADOR))

    # Dibujar puente
    if creciendo_puente:
        pygame.draw.line(screen, COLOR_PUENTE, (plataformas[plataforma_index].right, posicion_jugador_y),
                         (plataformas[plataforma_index].right, posicion_jugador_y - altura_puente), 5)
    elif longitud_puente > 0:
        pygame.draw.line(screen, COLOR_PUENTE, (plataformas[plataforma_index].right, posicion_jugador_y),
                         (plataformas[plataforma_index].right + longitud_puente, posicion_jugador_y), 5)

    pygame.display.flip()
    pygame.time.Clock().tick(60)  # 30 FPS

pygame.quit()