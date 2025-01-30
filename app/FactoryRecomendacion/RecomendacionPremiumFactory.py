from app.BuilderRecomendacion.RecomendacionBuilder import RecomendacionBuilder
from app.FactoryRecomendacion.RecomendacionFactory import RecomendacionFactory

class RecomendacionPremiumFactory(RecomendacionFactory):
    def crear_recomendacion(self, actividad, destino, reservas_dict, max_reservas, min_precio, temporada_match):
        puntaje = (
            (reservas_dict.get(actividad.id, 0) / max_reservas) * 0.5 +  # Mayor peso a la demanda
            (min_precio / actividad.precio) * 0.3 +  # Menor peso al precio
            temporada_match * 0.2
        )
        return (
            RecomendacionBuilder()
            .set_id(actividad.id)
            .set_nombre(actividad.nombre)
            .set_descripcion(actividad.descripcion)
            .set_precio(actividad.precio)
            .set_destino_id(actividad.destino_id)
            .set_destino_nombre(destino.nombre)
            .set_destino_temporada(destino.temporada_recomendada)
            .set_total_reservas(reservas_dict.get(actividad.id, 0))
            .set_puntaje(puntaje)
            .build()
        )