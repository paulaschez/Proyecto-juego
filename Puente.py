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

        # Cargar la imagen del puente
        self.segmento_original = pygame.image.load("media/puente/puente.jpeg").convert_alpha()
        self.segmento_original = pygame.transform.scale(self.segmento_original, (28,300))
        self.segmento_width = self.segmento_original.get_width()
        self.segmento_height = self.segmento_original.get_height()


    def actualizar(self):

        if self.creciendo:
            self.angulo = 90
            self.altura += self.velocidad_crecimiento
        elif self.cayendo:
            self.longitud = self.altura

            if self.angulo > 0:  # Sigue bajando el puente hasta que llegue a 0°
                self.angulo -= self.velocidad_caida / 3
            else:
                self.angulo = 0  # Es horizontal
                self.cayendo = False  # Termina la caída
                self.caido = True  # El puente terminó de caer


    def reiniciar(self):
        self.altura = 0
        self.longitud = 0
        self.angulo = 90
        self.creciendo = False
        self.cayendo = False
        self.caido = False

    def dibujar(self, pantalla, plataforma_actual):
        if self.creciendo or self.cayendo or self.angulo == 0:
            # Calcular la altura/longitud visible
            if self.creciendo:
                altura_visible = self.altura
            else:
                altura_visible = self.longitud

            # Recortar la parte visible del puente
            puente_visible = pygame.Surface((self.segmento_width, altura_visible), pygame.SRCALPHA)
            puente_visible.blit(
                self.segmento_original,
                (0, 0),
                (0, self.segmento_height - altura_visible, self.segmento_width, altura_visible)
            )

            # Calcular la posición del puente
            x_base = plataforma_actual.right
            y_base = constantes.POSICION_J_Y

            if self.angulo == 90:  # Vertical (creciendo)
                x_destino = x_base
                y_destino = y_base - altura_visible
            else:  # Cayendo o horizontal
                # Rotamos la imagen del puente
                puente_rotado = pygame.transform.rotate(puente_visible, self.angulo -90)

                # Calculamos las posiciones ajustadas para la base del puente


                x_destino = x_base
                y_destino = y_base - puente_rotado.get_height()

                puente_visible = puente_rotado

            # Dibujar el puente en la pantalla
            pantalla.blit(puente_visible, (x_destino- self.segmento_width, y_destino))


        """if self.creciendo:
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
                             (plataforma_actual.right + self.longitud, constantes.POSICION_J_Y), 5)"""