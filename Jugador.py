import constantes
import Utils


class Jugador:

    def __init__(self):

        # Atributos de la animacion
        self.cronometro_animacion = 0 # Controla el tiempo entre frames de la animación
        self.velocidad_animacion = constantes.VELOCIDAD_ANIMACION # Velocidad base de la animación
        self.indice_animacion = 0  # Índice del frame actual dentro de la animación

        # Diccionario que contiene todas las animaciones del jugador
        # Cada clave representa una acción, y cada valor es una lista de imágenes que componen la animación
        self.animaciones = {
            "caminando":Utils.load_animation(constantes.RUTA_DINO_CAMINANDO, 6, constantes.ESCALA),
            "reposo": Utils.load_animation(constantes.RUTA_DINO_REPOSO, 4, constantes.ESCALA),
            "muriendo": Utils.load_animation(constantes.RUTA_DINO_MURIENDO, 2, constantes.ESCALA)
        }

        # Posicion del jugador
        self.posicion_jugador_x = constantes.POSICION_J_X
        self.posicion_jugador_y = constantes.POSICION_J_Y

        # Estado del jugador: por defecto no se está moviendo
        self.moviendose = False

        # Array de imagenes (ruta a las imagenes) de la animacion que se este reproduciendo
        self.animacion_actual = self._get_animacion("reposo")

        # Rectángulo asociado al jugador en funcion de la imagen
        self.rect = self.animacion_actual[self.indice_animacion].get_rect()


    def draw(self, pantalla):
        """
        Dibuja el jugador en la pantalla en su posición actual.
        """
        pantalla.blit(self.animacion_actual[self.indice_animacion], # Imagen actual de la animación
                     (self.posicion_jugador_x, self.posicion_jugador_y - self.rect.height + 10), # Posición en pantalla
                     self.rect)

    def cambiar_animacion(self, accion):
        """
        Cambia la animación actual del jugador según la acción.
        :param accion: str - Puede ser 'caminando', 'reposo', 'muriendo'.
        """
        self.animacion_actual = self._get_animacion(accion) # Actualiza la animación actual
        self.indice_animacion = 0  # Reinicia la animación al primer frame


    def _get_animacion(self, accion):
        """
        Obtiene la lista de imágenes correspondiente a la acción especificada.
        Si no se encuentra la acción, retorna la animación "muriendo" por defecto.
        :param accion: str - Acción cuyo conjunto de imágenes se desea obtener.
        :return: list - Lista de imágenes de la animación.
        """
        if accion == "caminando":
            return self.animaciones.get("caminando")
        elif accion == "reposo":
            return self.animaciones.get("reposo")
        else:
            return self.animaciones.get("muriendo")



    def actualizar_animacion(self):
        """
        Actualiza el frame actual de la animación basado en el cronómetro.
        Cuando el cronómetro supera el límite, se avanza al siguiente frame.
        """

        # Incrementa el cronómetro en función de la velocidad de la animación actual
        self.cronometro_animacion += self._calcular_velocidad_animacion()

        # Cambia al siguiente frame si el cronómetro ha alcanzado el límite
        if self.cronometro_animacion >= 1:
            self.indice_animacion = (self.indice_animacion + 1) % len(self.animacion_actual)
            self.cronometro_animacion = 0 # Reinicia el cronómetro

    def _calcular_velocidad_animacion(self):
        """
        Calcula la velocidad de la animación dependiendo de la acción actual.
        Las animaciones más lentas tienen una velocidad menor.
        :return: float - Velocidad ajustada de la animación.
        """
        if self.animacion_actual == self.animaciones.get("caminando"):
           return self.velocidad_animacion
        elif self.animacion_actual == self.animaciones.get("reposo"):
            return self.velocidad_animacion / 2
        else:
            return self.velocidad_animacion / 4

