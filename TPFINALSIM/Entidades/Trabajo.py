import random

class Trabajo:
    def __init__(self, id, directivo, llegada):
        self.id = id
        self.directivo = directivo
        self.llegada = llegada
        self.inicio_atencion = None
        self.fin_atencion = None
        self.tiempo_servicio = None
        self.requiere_reparacion = False
        self.estado = "EEA"

    @staticmethod
    def generar_tiempo_llegada(media_llegada):
        return random.expovariate(1 / media_llegada)

    @staticmethod
    def generar_tiempo_servicio():
        return random.uniform(5, 10)

    @staticmethod
    def tiene_error(probabilidad_error=0.06):
        return random.random() < probabilidad_error
