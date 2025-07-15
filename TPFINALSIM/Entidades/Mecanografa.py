class Mecanografa:
    def __init__(self):
        self.estado = "L"
        self.trabajo_actual = None

    def esta_libre(self):
        return self.estado == "L"

    def ocupar(self, trabajo):
        self.trabajo_actual = trabajo
        self.estado = "OP" if trabajo.directivo == 1 else "ON"

    def liberar(self):
        self.trabajo_actual = None
        self.estado = "L"
