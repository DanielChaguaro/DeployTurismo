from abc import ABC, abstractmethod

class RecomendacionFactory(ABC):
    @abstractmethod
    def crear_recomendacion(self, actividad, destino, reservas_dict, max_reservas, min_precio, temporada_match):
        pass
#class RecomendacionFactory:
#    @staticmethod
#    def crear_recomendacion(id, nombre, descripcion, precio, destino_id, destino_nombre, destino_temporada, total_reservas, puntaje):
#        """Crea y retorna una instancia de Recomendacion."""
#        return Recomendacion(
#            id=id,
#            nombre=nombre,
#            descripcion=descripcion,
#            precio=precio,
#            destino_id=destino_id,
#            destino_nombre=destino_nombre,
#            destino_temporada=destino_temporada,
#            total_reservas=total_reservas,
#            puntaje=puntaje
#        )
        
