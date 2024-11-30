import pygame

import constantes


class PantallaGameOver:
    def __init__(self):
        self.fuente = pygame.font.Font( None, 50)
        self.texto_game_over = self.fuente.render("GAME OVER", True, (255, 0, 0))
        self.texto_reintentar = self.fuente.render("Presiona 'R' para reiniciar", True, (255, 255, 255))
        self.texto_salir = self.fuente.render("Presiona 'ESC' para salir", True, (255, 255, 255))

        recuadro_ancho = constantes.ANCHO_PANTALLA / 1.5
        recuadro_alto = constantes.ALTO_PANTALLA / 2  #
        self.recuadro_opciones = pygame.Surface((recuadro_ancho, recuadro_alto))
        self.recuadro_opciones.set_alpha(150)
        self.recuadro_opciones.fill((0, 0, 0))

    def mostrar(self, pantalla):
        # Dibujar el recuadro sobre la pantalla en el centro
        recuadro_x = (constantes.ANCHO_PANTALLA - self.recuadro_opciones.get_width()) // 2
        recuadro_y = (constantes.ALTO_PANTALLA - self.recuadro_opciones.get_height()) // 2
        pantalla.blit(self.recuadro_opciones, (recuadro_x, recuadro_y))

        # Dibujar los textos en el recuadro
        pantalla.blit(self.texto_game_over, (constantes.ANCHO_PANTALLA / 2 - self.texto_game_over.get_width() / 2, constantes.ALTO_PANTALLA / 3))
        pantalla.blit(self.texto_reintentar, (constantes.ANCHO_PANTALLA / 2 - self.texto_reintentar.get_width() / 2, constantes.ALTO_PANTALLA / 2 + 50))
        pantalla.blit(self.texto_salir, (constantes.ANCHO_PANTALLA / 2 - self.texto_salir.get_width() / 2, constantes.ALTO_PANTALLA / 2 + 100))

    def manejar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return 'reiniciar'
            elif event.key == pygame.K_ESCAPE:
                return 'salir'
        return None