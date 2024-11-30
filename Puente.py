import math
import pygame
import constantes

class Puente:
    def __init__(self):
        self.altura = 0
        self.longitud = 0
        self.angulo = 90

        self.creciendo = False
        self.cayendo = False
        self.caido = False

        self.velocidad_crecimiento = constantes.VELOCIDAD_CRECIMIENTO_PUENTE
        self.velocidad_caida = constantes.VELOCIDAD_CRECIMIENTO_PUENTE



    def actualizar(self):

        if self.creciendo:
            print(f"EL PUENTE ESTA CRECIENDO")
            self.angulo = 90
            self.altura += self.velocidad_crecimiento
        elif self.cayendo:
            self.longitud = self.altura

            if self.angulo > 0:  # Sigue bajando el puente hasta que llegue a 0°
                self.angulo -= self.velocidad_caida
            else:
                self.angulo = 0  # Es horizontal
                self.cayendo = False  # Termina la caída
                self.caido = True  # El puente terminó de caer

        """elif self.caido:
            self.altura = 0 #Se reinicia la altura
            self.caido = False"""

    def reiniciar(self):
        self.altura = 0
        self.longitud = 0
        self.angulo = 90
        self.creciendo = False
        self.cayendo = False
        self.caido = False

    def dibujar(self, pantalla, plataforma_actual):
        if self.creciendo:
            pygame.draw.line(pantalla, constantes.COLOR_PUENTE, (plataforma_actual.right, constantes.POSICION_J_Y),
                             (plataforma_actual.right, constantes.POSICION_J_Y - self.altura), 5)

        elif self.cayendo:
            extremo_x = plataforma_actual.right + + self.longitud * math.cos(math.radians(self.angulo))
            extremo_y = constantes.POSICION_J_Y - self.longitud * math.sin(math.radians(self.angulo))
            pygame.draw.line(pantalla, constantes.COLOR_PUENTE,
                             (plataforma_actual.right, constantes.POSICION_J_Y),
                             (extremo_x, extremo_y), 5)
        elif self.angulo == 0:
            pygame.draw.line(pantalla, constantes.COLOR_PUENTE, (plataforma_actual.right, constantes.POSICION_J_Y),
                             (plataforma_actual.right + self.longitud, constantes.POSICION_J_Y), 5)


