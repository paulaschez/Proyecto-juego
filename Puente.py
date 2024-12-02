import math
import pygame
import constantes

class Puente:
    def __init__(self):

        # Atributos iniciales del puente
        self.altura = 0 # Altura actual del puente mientras crece
        self.longitud = 0 # Longitud final del puente después de caer
        self.angulo = 90 # Angulo del puente (90 vertical, 0, horizontal)

        # Estados del puente
        self.creciendo = False # Indica si esta creciendo
        self.cayendo = False # Indica si esta cayendo
        self.caido = False # Indica si ha terminado de caer

        # Velocidades de crecimiento y caída
        self.velocidad_crecimiento = constantes.VELOCIDAD_CRECIMIENTO_PUENTE
        self.velocidad_caida = constantes.VELOCIDAD_CAIDA_PUENTE

        # Carga la imagen del puente
        self.imagen_puente_completo = pygame.image.load(constantes.RUTA_IMG_PUENTE).convert_alpha()

        # Dimensiones de la imagen del puente
        self.puente_completo_width = self.imagen_puente_completo.get_width()
        self.puente_completo_height = self.imagen_puente_completo.get_height()

    """ Metodo para actualizar la longitud, altura, angulo y velocidad de crecimiento el puente"""
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
            self.angulo = 90 # El puente se mantiene vertical
            self.altura += self.velocidad_crecimiento # Incrementa la altura

        elif self.cayendo:
            self.longitud = self.altura # Guarda la altura como la longitud

            # Si aun no esta horizontal
            if self.angulo > 0:  # Sigue bajando el puente hasta que llegue a 0°
                self.angulo -= self.velocidad_caida / 3 # Reduce el angulo poco a poco
            else:
                self.angulo = 0  # Es horizontal
                self.cayendo = False  # Termina la caída
                self.caido = True  # El puente terminó de caer


    # Metodo para reiniciar lo valores del puente a su valor al iniciar
    def reiniciar(self):
        self.altura = 0
        self.longitud = 0
        self.angulo = 90
        self.creciendo = False
        self.cayendo = False
        self.caido = False

    # Metodo para dibujar el puente
    def dibujar(self, pantalla, plataforma_actual):

        # Dibujar el puente solo si está creciendo, cayendo o completamente horizontal
        if self.creciendo or self.cayendo or self.angulo == 0:
            # Calcular la altura/longitud visible
            if self.creciendo:
                tamanio_adaptado = self.altura # Mientras crece, usar la altura
            else:
                tamanio_adaptado = self.longitud # Después de caer, usar la longitud


            # Crear una superficie con la parte visible del puente
            puente_tamanio_adaptado = pygame.Surface((self.puente_completo_width, tamanio_adaptado), pygame.SRCALPHA)
            puente_tamanio_adaptado.blit(
                self.imagen_puente_completo,
                (0, 0),
                (0, self.puente_completo_height - tamanio_adaptado, self.puente_completo_width, tamanio_adaptado)
            )

            # Calcular la posición base del puente (donde comienza a dibujarse)
            x_base = plataforma_actual.right
            y_base = constantes.POSICION_J_Y

            if self.angulo == 90:  # Vertical (creciendo)
                x_destino = x_base # El puente está alineado verticalmente
                y_destino = y_base - tamanio_adaptado  # Se dibuja hacia arriba desde la base
            else:  # Cayendo o horizontal
                # Rotamos la imagen del puente
                puente_rotado = pygame.transform.rotate(puente_tamanio_adaptado, self.angulo -90)

                # Calculamos las posiciones ajustadas para la base del puente
                x_destino = x_base
                y_destino = y_base - puente_rotado.get_height()

                puente_tamanio_adaptado = puente_rotado # Usar la imagen rotada

            # Dibujar el puente en la pantalla
            pantalla.blit(puente_tamanio_adaptado, (x_destino - self.puente_completo_width, y_destino))


