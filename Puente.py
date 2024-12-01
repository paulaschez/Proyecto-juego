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
        self.velocidad_caida = constantes.VELOCIDAD_CAIDA_PUENTE

        # Cargar la imagen del puente
        self.imagen_puente_completo = pygame.image.load("media/graficos/puente/watewatecontomate.png").convert_alpha()


        self.puente_completo_width = self.imagen_puente_completo.get_width()
        self.puente_completo_height = self.imagen_puente_completo.get_height()


    def actualizar(self, puntuacion):

        # Ajustar la velocidad de crecimiento según la puntuación
        if puntuacion > 50:
            self.velocidad_crecimiento = 15
        elif puntuacion > 30:
            self.velocidad_crecimiento = 12
        elif puntuacion > 10:
            self.velocidad_crecimiento = 10
        elif puntuacion > 5:
            self.velocidad_crecimiento = 7

        # Logica de crecimiento del puente
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
                tamanio_adaptado = self.altura
            else:
                tamanio_adaptado = self.longitud


            # Recortar la parte visible del puente
            puente_tamanio_adaptado = pygame.Surface((self.puente_completo_width, tamanio_adaptado), pygame.SRCALPHA)
            puente_tamanio_adaptado.blit(
                self.imagen_puente_completo,
                (0, 0),
                (0, self.puente_completo_height - tamanio_adaptado, self.puente_completo_width, tamanio_adaptado)
            )

            # Calcular la posición del puente
            x_base = plataforma_actual.right
            y_base = constantes.POSICION_J_Y

            if self.angulo == 90:  # Vertical (creciendo)
                x_destino = x_base
                y_destino = y_base - tamanio_adaptado
            else:  # Cayendo o horizontal
                # Rotamos la imagen del puente
                puente_rotado = pygame.transform.rotate(puente_tamanio_adaptado, self.angulo -90)

                # Calculamos las posiciones ajustadas para la base del puente
                x_destino = x_base
                y_destino = y_base - puente_rotado.get_height()

                puente_tamanio_adaptado = puente_rotado

            # Dibujar el puente en la pantalla
            pantalla.blit(puente_tamanio_adaptado, (x_destino - self.puente_completo_width, y_destino))


