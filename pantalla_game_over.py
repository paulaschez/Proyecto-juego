import pygame
import constantes
from Utils import cargar

class PantallaGameOver:
    def __init__(self):
        # Configuración de fuentes
        self.fuente = pygame.font.Font(constantes.RUTA_FUENTE, 15) # Fuente para las instrucciones de reintentar o salir
        self.fuente_t = pygame.font.Font(constantes.RUTA_FUENTE, 60) # Fuente para el texto de Game Over
        self.fuente_pt = pygame.font.Font(constantes.RUTA_FUENTE, 30) # Fuente para la puntuacion maxima

        # Carga de la imagen del cartel
        self.cartel = pygame.image.load(constantes.RUTA_IMG_CARTEL)
        # Posición inicial del cartel fuera de la pantalla
        self.pos_x_cartel = (constantes.ANCHO_PANTALLA - self.cartel.get_width()) / 2
        self.pos_y_cartel = -self.cartel.get_height()

        # Obtención de la puntuacion maxima del archivo json
        self.puntuacion_maxima = cargar()

        # Textos
        self.texto_game_over = self.fuente_t.render("GAME OVER", True, constantes.ROJO)
        self.texto_reintentar = self.fuente.render("Presiona 'R' para reiniciar", True, constantes.BLANCO)
        self.texto_salir = self.fuente.render("Presiona 'ESC' para salir", True, constantes.BLANCO)
        self.texto_puntuacion_maxima = self.fuente_pt.render(f"Puntuacion maxima: {self.puntuacion_maxima}", True,constantes.BLANCO )


    def reiniciar(self):
        self.pos_y_cartel = -self.cartel.get_height()

    def actualizar(self):
        # Mover el cartel hacia abajo hasta que llegue a su posición final
        if self.pos_y_cartel < 0:
            self.pos_y_cartel += constantes.VELOCIDAD_DESPLAZAMIENTO_PANTALLA * 2

        self.puntuacion_maxima = cargar()
        self.texto_puntuacion_maxima = self.fuente_pt.render(f"Puntuacion maxima: {self.puntuacion_maxima}", True,(255, 255, 255) )




    def mostrar(self, pantalla):
        # Dibujar el cartel en su posición actual
        pantalla.blit(self.cartel, (self.pos_x_cartel, self.pos_y_cartel))

        # Posiciones dinámicas de los textos basadas en la posición del cartel
        pos_y_texto_game_over = self.pos_y_cartel + self.cartel.get_height()/1.85
        pos_y_texto_puntuacion_max = pos_y_texto_game_over + 75
        pos_y_texto_reintentar = pos_y_texto_puntuacion_max + 50
        pos_y_texto_salir = pos_y_texto_reintentar + 25

        # Dibujar los textos
        pantalla.blit(self.texto_game_over,
                      (constantes.ANCHO_PANTALLA / 2 - self.texto_game_over.get_width() / 2, pos_y_texto_game_over))
        pantalla.blit(self.texto_puntuacion_maxima,
                      (constantes.ANCHO_PANTALLA / 2 - self.texto_puntuacion_maxima.get_width() / 2, pos_y_texto_puntuacion_max))
        pantalla.blit(self.texto_reintentar,
                      (constantes.ANCHO_PANTALLA / 2 - self.texto_reintentar.get_width() / 2, pos_y_texto_reintentar))
        pantalla.blit(self.texto_salir,
                      (constantes.ANCHO_PANTALLA / 2 - self.texto_salir.get_width() / 2, pos_y_texto_salir))


     # Metodo para manejar los eventos durante el estado de Game Over.
    def manejar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: # Si se presiona 'R', se reinicia el juego
                return "reiniciar"
            elif event.key == pygame.K_ESCAPE: # Si se presiona 'ESC', se solicita salir del juego
                return "salir"
        return None # Si no se presiona ninguna tecla relevante, no se realiza ninguna acción
