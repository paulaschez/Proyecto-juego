import pygame

import constantes


class Plataforma:
    def __init__(self, pos_x, ancho):
        self.rect = pygame.Rect(pos_x, constantes.POSICION_J_Y, ancho, constantes.ALTO_PLATAFORMA)

    def draw(self, pantalla):
        pygame.draw.rect(pantalla, constantes.COLOR_PLATAFORMA, self.rect)


