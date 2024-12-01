import json
import os

import pygame

ARCHIVO_ESTADISTICAS = "estadisticas.json"


# Función para crear un array con las imagenes de una animacion
def load_animation(path, num_images, scale: (70, 80)):
    """Carga y escala una serie de imágenes para la animación."""
    images = []
    for i in range(1, num_images + 1):
        img = pygame.image.load(f"{path}{i}.png")
        images.append(pygame.transform.scale(img, scale))
    return images


# Función para inicializar las estadísticas si el archivo no existe
def inicializar():
    return {
        "puntuacion_max": 0
    }

# Función para guardar estadísticas después de cada partida
def guardar(puntuacion):
    # Cargar estadísticas existentes o inicializarlas si el archivo no existe
    if os.path.exists(ARCHIVO_ESTADISTICAS):
        with open(ARCHIVO_ESTADISTICAS, "r") as file:
            estadisticas = json.load(file)
    else:
        estadisticas = inicializar()

    # Actualizar el mejor puntaje si el puntaje actual es mayor
    if puntuacion > estadisticas["puntuacion_max"]:
        estadisticas["puntuacion_max"] = puntuacion

        # Guardar estadísticas actualizadas en el archivo
    with open(ARCHIVO_ESTADISTICAS, "w") as file:
        json.dump(estadisticas, file)

# Función para cargar estadísticas
def cargar():
    if os.path.exists(ARCHIVO_ESTADISTICAS):
        with open(ARCHIVO_ESTADISTICAS, "r") as file:
            estadisticas = json.load(file)
            return estadisticas["puntuacion_max"]
    return inicializar()
