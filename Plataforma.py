import pygame

import constantes


class Plataforma:
    def __init__(self, pos_x, ancho):
        self.rect = pygame.Rect(pos_x, constantes.POSICION_J_Y, ancho, constantes.ALTO_PLATAFORMA)


        self.mitad = self.rect.width / 2

        self.ancho = ancho
        self.pos_x = pos_x

        self.centro_completo = pygame.image.load("media/graficos/plataforma/plat_central.png").convert_alpha()
        self.centro_ancho = self.centro_completo.get_width()
        self.centro_alto = self.centro_completo.get_height()

        self.borde_izquierdo = pygame.image.load("media/graficos/plataforma/plat_izquierda.png").convert_alpha()
        self.borde_derecho = pygame.image.load("media/graficos/plataforma/plat_derecha.png").convert_alpha()

    def actualizar(self):
        # Actualizar la posición de la plataforma (desplazarse a la izquierda)
        self.pos_x -= constantes.VELOCIDAD_DESPLAZAMIENTO_PANTALLA
        self.rect.x = self.pos_x

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
