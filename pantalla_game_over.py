import pygame

import constantes


class PantallaGameOver:
    def __init__(self):
        # Configuración de fuentes y cartel
        self.fuente = pygame.font.Font(constantes.RUTA_FUENTE, 30)
        self.fuente_t = pygame.font.Font(constantes.RUTA_FUENTE, 50)
        self.cartel = pygame.image.load(constantes.RUTA_IMG_CARTEL)

        # Posición inicial del cartel fuera de la pantalla
        self.pos_x_cartel = (constantes.ANCHO_PANTALLA - self.cartel.get_width()) / 2
        self.pos_y_cartel = -self.cartel.get_height()

        # Textos
        self.texto_game_over = self.fuente_t.render("GAME OVER", True, (255, 0, 0))
        self.texto_reintentar = self.fuente.render("Presiona 'R' para reiniciar", True, (255, 255, 255))
        self.texto_salir = self.fuente.render("Presiona 'ESC' para salir", True, (255, 255, 255))

    def reiniciar(self):
        self.pos_y_cartel = -self.cartel.get_height()

    def actualizar(self):
        # Mover el cartel hacia abajo hasta que llegue a su posición final
        if self.pos_y_cartel < 0:
            self.pos_y_cartel += constantes.VELOCIDAD_DESPLAZAMIENTO_PANTALLA * 2

    def mostrar(self, pantalla):
        # Dibujar el cartel en su posición actual
        pantalla.blit(self.cartel, (self.pos_x_cartel, self.pos_y_cartel))

        # Posiciones dinámicas de los textos basadas en la posición del cartel
        pos_y_texto_game_over = self.pos_y_cartel + self.cartel.get_height()/2
        pos_y_texto_reintentar = pos_y_texto_game_over + 75
        pos_y_texto_salir = pos_y_texto_reintentar + 50

        # Dibujar los textos
        pantalla.blit(self.texto_game_over,
                      (constantes.ANCHO_PANTALLA / 2 - self.texto_game_over.get_width() / 2, pos_y_texto_game_over))
        pantalla.blit(self.texto_reintentar,
                      (constantes.ANCHO_PANTALLA / 2 - self.texto_reintentar.get_width() / 2, pos_y_texto_reintentar))
        pantalla.blit(self.texto_salir,
                      (constantes.ANCHO_PANTALLA / 2 - self.texto_salir.get_width() / 2, pos_y_texto_salir))

    def manejar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return 'reiniciar'
            elif event.key == pygame.K_ESCAPE:
                return 'salir'
        return None