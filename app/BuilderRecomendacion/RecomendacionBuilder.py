from flask import session, render_template , request
from app.models.Recomendacion import Recomendacion

class RecomendacionBuilder:
    def __init__(self):
        self.recomendacion = Recomendacion()

    def set_id(self, id):
        self.recomendacion.id = id
        return self

    def set_nombre(self, nombre):
        self.recomendacion.nombre = nombre
        return self

    def set_descripcion(self, descripcion):
        self.recomendacion.descripcion = descripcion
        return self

    def set_precio(self, precio):
        self.recomendacion.precio = precio
        return self

    def set_destino_id(self, destino_id):
        self.recomendacion.destino_id = destino_id
        return self

    def set_destino_nombre(self, destino_nombre):
        self.recomendacion.destino_nombre = destino_nombre
        return self

    def set_destino_temporada(self, destino_temporada):
        self.recomendacion.destino_temporada = destino_temporada
        return self

    def set_total_reservas(self, total_reservas):
        self.recomendacion.total_reservas = total_reservas
        return self

    def set_puntaje(self, puntaje):
        self.recomendacion.puntaje = puntaje
        return self

    def build(self):
        return self.recomendacion