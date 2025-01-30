
from app.models.Actividad import Actividad
from app.models.db import db
from app.models.Usuario import Usuario
from app.models.Reserva import Reserva
from app.models.Destino import Destino
from sqlalchemy import func,text

class RecomendacionService:
    def __init__(self, factory):
        self.factory = factory

    def obtener_preferencias_usuario(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        return usuario.preferencias.split(',') if usuario.preferencias else []

    def filtrar_actividades_por_preferencias(self, actividades, preferencias):
        actividades_filtradas = []
        for actividad in actividades:
            for destino in Destino.query.all():
                if actividad.destino_id == destino.id:
                    for preferencia in preferencias:
                        if preferencia.lower() in actividad.descripcion.lower():
                            actividades_filtradas.append((actividad, destino))
        return actividades_filtradas

    def calcular_puntaje(self, actividad, destino, reservas_dict, max_reservas, min_precio, temporada_match):
        return self.factory.crear_recomendacion(
            actividad=actividad,
            destino=destino,
            reservas_dict=reservas_dict,
            max_reservas=max_reservas,
            min_precio=min_precio,
            temporada_match=temporada_match
        )

    def generar_recomendaciones(self, usuario_id, actividades, fecha_inicial, fecha_final):
        preferencias = self.obtener_preferencias_usuario(usuario_id)
        actividades_filtradas = self.filtrar_actividades_por_preferencias(actividades, preferencias)

        temporada_actual = self.obtener_temporada_actual(fecha_inicial)
        reservas_dict, max_reservas, min_precio = self.obtener_datos_reservas(fecha_inicial, fecha_final)

        recomendaciones = []
        actividades_agregadas = set()
        for actividad, destino in actividades_filtradas:
            if actividad.id not in actividades_agregadas:
                temporada_match = 1 if temporada_actual and (temporada_actual in destino.temporada_recomendada or 'todo el año' in destino.temporada_recomendada) else 0
                recomendacion = self.calcular_puntaje(actividad, destino, reservas_dict, max_reservas, min_precio, temporada_match)
                recomendaciones.append(recomendacion)
                actividades_agregadas.add(actividad.id)

        return sorted(recomendaciones, key=lambda x: x.puntaje, reverse=True)

    def obtener_temporada_actual(self, fecha_inicial):
        if fecha_inicial:
            mes_inicial = fecha_inicial.month
            if mes_inicial in [12, 1, 2]:
                return "invierno"
            elif mes_inicial in [3, 4, 5]:
                return "primavera"
            elif mes_inicial in [6, 7, 8]:
                return "verano"
            else:
                return "otoño"
        return None

    def obtener_datos_reservas(self, fecha_inicial, fecha_final):
        reservas_por_actividad = (
            db.session.query(Reserva.actividad_id, func.count(Reserva.id).label("total_reservas"))
            .filter(Reserva.fecha >= fecha_inicial)
            .filter(Reserva.fecha <= fecha_final)
            .group_by(Reserva.actividad_id)
            .all()
        )
        reservas_dict = {reserva.actividad_id: reserva.total_reservas for reserva in reservas_por_actividad}
        max_reservas = max(reservas_dict.values(), default=1)
        min_precio = min([actividad.precio for actividad in Actividad.query.all()], default=1)
        return reservas_dict, max_reservas, min_precio