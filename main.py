import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Puentes Infinito")

# Colores
COLOR_FONDO = (135, 206, 235)  # Azul cielo
COLOR_PLATAFORMA = (100, 100, 100)  # Gris oscuro
COLOR_JUGADOR = (255, 69, 0)  # Naranja
COLOR_PUENTE = (0, 0, 0)  # Negro

# Parámetros del juego
TAMAÑO_JUGADOR = 20
VELOCIDAD_CRECE_PUENTE = 5
VELOCIDAD_DESPLAZAMIENTO_PANTALLA = 5
posicion_jugador_x = 100
posicion_jugador_y = ALTO - 100

# Listas de plataformas y variables del puente
plataformas = []
altura_puente = 0
creciendo_puente = False
puente_caido = False
longitud_puente = 0
moviendo_jugador = False
plataforma_index = 0
desplazamiento_completo = False



# Generación de plataformas aleatorias
def generar_plataforma(x_pos):
    while True:
        ancho = random.randint(50, 150)
        yield pygame.Rect(x_pos, posicion_jugador_y, ancho, 20)

# Inicialización de plataformas
x_inicial = posicion_jugador_x
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
        if posicion_jugador_x < ANCHO - 200:  # Si el jugador está lejos del borde derecho
            posicion_jugador_x += VELOCIDAD_DESPLAZAMIENTO_PANTALLA
        else:

            # Desplaza todas las plataformas hacia la izquierda
            for plataforma in plataformas:
                plataforma.x -= VELOCIDAD_DESPLAZAMIENTO_PANTALLA

            # Desplaza el puente también
            longitud_puente -= VELOCIDAD_DESPLAZAMIENTO_PANTALLA

            # Generar nuevas plataformas si es necesario
            # Verificar si faltan plataformas en el espacio visible

        # Si el jugador llega a la siguiente plataforma
        if plataformas[plataforma_index].right + longitud_puente <= posicion_jugador_x + TAMAÑO_JUGADOR:
            # Alinea el jugador con la siguiente plataforma
            plataforma_index += 1
            posicion_jugador_x = plataformas[plataforma_index].left
            moviendo_jugador = False  # Deja de mover al jugador
            longitud_puente = 0  # Reinicia la longitud del puente

        # Posicion a partir de la cual se desplaza tó
        if posicion_jugador_x >= ANCHO - 400:
            desplazamiento_completo = True

        # Se desplaza tó
        if desplazamiento_completo:
            # Calcular cuánto se debe desplazar para alinear la plataforma actual al inicio
            desplazamiento = plataformas[plataforma_index].left

            # Desplaza todas las plataformas
            for plataforma in plataformas:
                plataforma.x -= desplazamiento

            # Ajusta la posición del jugador
            posicion_jugador_x -= desplazamiento

            # Desactiva el desplazamiento completo
            desplazamiento_completo = False

    while len(plataformas) < 5:
        print("ha entrao")
        # Generar nueva plataforma al final
        nueva_x = plataformas[-1].right + random.randint(100, 200)
        plataformas.append(next(generar_plataforma(nueva_x)))

    if plataformas[0].right < 0:
        print("se ha eliminao")
        plataformas.pop(0)
        print(len(plataformas))
        plataforma_index-=1

    # Dibujado de la pantalla
    screen.fill(COLOR_FONDO)

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
    pygame.time.Clock().tick(30)  # 30 FPS

pygame.quit()