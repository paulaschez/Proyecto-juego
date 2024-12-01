import constantes
import Utils


class Jugador:

    def __init__(self):

        # Atributos de la animacion
        self.cronometro_animacion = 0
        self.velocidad_animacion = constantes.VELOCIDAD_ANIMACION
        self.indice_animacion = 0

        # Mapa con las animaciones disponibles
        self.animaciones = {
            "caminando":Utils.load_animation(constantes.RUTA_DINO_CAMINANDO, 6, constantes.ESCALA),
            "reposo": Utils.load_animation(constantes.RUTA_DINO_REPOSO, 4, constantes.ESCALA),
            "muriendo": Utils.load_animation(constantes.RUTA_DINO_MURIENDO, 2, constantes.ESCALA)
        }

        # Posicion del jugador
        self.posicion_jugador_x = constantes.POSICION_J_X
        self.posicion_jugador_y = constantes.POSICION_J_Y

        # Estado del jugador
        self.moviendose = False

        # Array de imagenes (ruta a las imagenes) de la animacion que se este reproduciendo
        self.animacion_actual = self._get_animacion("reposo")

        self.rect = self.animacion_actual[self.indice_animacion].get_rect()




    def draw(self, pantalla):
        pantalla.blit(self.animacion_actual[self.indice_animacion], (self.posicion_jugador_x, self.posicion_jugador_y - self.rect.height + 10), self.rect)

    def cambiar_animacion(self, accion):
        """
        Cambia la animación actual del jugador según la acción.
        :param accion: str - Puede ser 'caminando', 'reposo', 'muriendo'.
        """
        self.animacion_actual = self._get_animacion(accion)
        self.indice_animacion = 0  # Reinicia la animación al primer frame


    def _get_animacion(self, accion):

        if accion == "caminando":
            return self.animaciones.get("caminando")
        elif accion == "reposo":
            return self.animaciones.get("reposo")
        else:
            return self.animaciones.get("muriendo")



    def actualizar_animacion(self):

        # Obtiene la velocidad a la que ira la animacion
        self.cronometro_animacion += self._calcular_velocidad_animacion()

        # Segun el tipo de animacion se reiniciara cuando terminen las imagenes
        if self.cronometro_animacion >= 1:
            self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion_actual)
            self.cronometro_animacion = 0

    def _calcular_velocidad_animacion(self):

        if self.animacion_actual == self.animaciones.get("caminando"):
           return self.velocidad_animacion
        elif self.animacion_actual == self.animaciones.get("reposo"):
            return self.velocidad_animacion / 2
        else:
            return self.velocidad_animacion / 4

