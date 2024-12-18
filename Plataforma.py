import pygame
import constantes

class Plataforma:
    def __init__(self, pos_x, ancho):

        # Define un rectángulo que representa la plataforma (posición y dimensiones)
        self.rect = pygame.Rect(pos_x, constantes.POSICION_J_Y, ancho, constantes.ALTO_PLATAFORMA)

        # Guarda el ancho y la posición X inicial de la plataforma
        self.ancho = ancho
        self.pos_x = pos_x

        # Carga las imágenes de las diferentes partes de la plataforma
        self.centro_completo = pygame.image.load(constantes.RUTA_IMG_PLAT_CENT).convert_alpha()
        self.borde_izquierdo = pygame.image.load(constantes.RUTA_IMG_PLAT_IZQ).convert_alpha()
        self.borde_derecho = pygame.image.load(constantes.RUTA_IMG_PLAT_DER).convert_alpha()

        # Obtiene las medidas de la imagen del centro
        self.centro_ancho = self.centro_completo.get_width()
        self.centro_alto = self.centro_completo.get_height()



    def actualizar(self):
        # Actualizar la posición de la plataforma (desplazarse a la izquierda)
        self.pos_x -= constantes.VELOCIDAD_DESPLAZAMIENTO_PANTALLA
        self.rect.x = self.pos_x

    """
       Dibuja la plataforma en la pantalla usando las imágenes de sus partes:
       el borde izquierdo, el centro (recortado según sea necesario) y el borde derecho.
    """
    def draw(self, pantalla, vel_desplazamiento=0):

        # Calcular el ancho necesario de la sección central
        ancho_plat_centro = (
                self.ancho - self.borde_derecho.get_width() - self.borde_izquierdo.get_width()
        )

        # Crear una nueva superficie del tamaño de la sección central
        centro_recortado = pygame.Surface(
            (ancho_plat_centro, self.centro_alto), pygame.SRCALPHA
        )

        # Copiar la parte visible de la sección central a la nueva superficie
        centro_recortado.blit(
            self.centro_completo,
            (0, 0),  # Posición donde copiar en la nueva superficie
            (0, 0, ancho_plat_centro, self.centro_alto),  # Rectángulo de la imagen original a copiar
        )

        # Dibujar el borde izquierdo
        pantalla.blit(self.borde_izquierdo, (self.pos_x - vel_desplazamiento, constantes.POSICION_J_Y))

        # Dibujar la sección central recortada
        pantalla.blit(
            centro_recortado,
            (self.pos_x - vel_desplazamiento + self.borde_izquierdo.get_width(), constantes.POSICION_J_Y),
        )

        # Dibujar el borde derecho
        pantalla.blit(
            self.borde_derecho,
            (
                self.pos_x - vel_desplazamiento + self.ancho - self.borde_derecho.get_width(),
                constantes.POSICION_J_Y,
            ),
        )
