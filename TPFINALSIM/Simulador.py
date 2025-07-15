import random
from Entidades.Trabajo import Trabajo
from Entidades.Mecanografa import Mecanografa

class Simulador:
    def __init__(self, media_llegada, tiempo_reparacion, trabajos_objetivo):
        self.media_llegada = media_llegada
        self.tiempo_reparacion = tiempo_reparacion
        self.trabajos_objetivo = trabajos_objetivo

    def ejecutar(self, iteraciones=1):
        resultados = []
        for _ in range(iteraciones):
            resultados.append(self._simular_corrida())
        return resultados

    def _simular_corrida(self):
        reloj = 0
        trabajos_completados = 0
        trabajos = []
        cola = []
        llegadas = {i: Trabajo.generar_tiempo_llegada(self.media_llegada) for i in [1, 2, 3]}
        mecanografa = Mecanografa()
        contador_trabajos = 0
        acum_espera = 0
        acum_tiempo_sistema = 0

        while trabajos_completados < self.trabajos_objetivo:
            eventos = [(k, v) for k, v in llegadas.items()]
            if mecanografa.trabajo_actual:
                eventos.append(("fin", mecanografa.trabajo_actual.fin_atencion))
            evento_tipo, evento_tiempo = min(eventos, key=lambda x: x[1])
            reloj = evento_tiempo

            if evento_tipo == "fin":
                t = mecanografa.trabajo_actual
                t.fin_atencion = reloj
                t.estado = "Finalizado"
                trabajos_completados += 1
                acum_espera += t.inicio_atencion - t.llegada
                acum_tiempo_sistema += t.fin_atencion - t.llegada
                mecanografa.liberar()
            else:
                directivo = evento_tipo
                contador_trabajos += 1
                t = Trabajo(contador_trabajos, directivo, reloj)
                trabajos.append(t)
                llegadas[directivo] = reloj + Trabajo.generar_tiempo_llegada(self.media_llegada)

                if mecanografa.esta_libre():
                    t.estado = "SA"
                    t.inicio_atencion = reloj
                    t.tiempo_servicio = Trabajo.generar_tiempo_servicio()
                    if Trabajo.tiene_error():
                        t.requiere_reparacion = True
                        t.fin_atencion = reloj + (t.tiempo_servicio / 2) + self.tiempo_reparacion + (t.tiempo_servicio / 2)
                    else:
                        t.fin_atencion = reloj + t.tiempo_servicio
                    mecanografa.ocupar(t)
                else:
                    cola.append(t)

        # Cálculos finales
        Wq = acum_espera / trabajos_completados
        W = acum_tiempo_sistema / trabajos_completados
        lambda_efectiva = trabajos_completados / reloj
        Lq = lambda_efectiva * Wq

        return {
            "Wq": round(Wq, 2),
            "W": round(W, 2),
            "lambda_efectiva": round(lambda_efectiva, 4),
            "Lq": round(Lq, 2),
            "tiempo_total_simulado": round(reloj, 2),
            "trabajos": [
                {
                    "id": t.id,
                    "directivo": t.directivo,
                    "llegada": round(t.llegada, 2),
                    "inicio": round(t.inicio_atencion, 2),
                    "fin": round(t.fin_atencion, 2),
                    "espera": round(t.inicio_atencion - t.llegada, 2),
                    "total_sistema": round(t.fin_atencion - t.llegada, 2),
                    "reparacion": t.requiere_reparacion
                }
                for t in trabajos if t.fin_atencion
            ]
        }
