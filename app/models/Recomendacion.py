class Recomendacion:
    def __init__(self):
        self.id = None
        self.nombre = None
        self.descripcion = None
        self.precio = None
        self.destino_id = None
        self.destino_nombre = None
        self.destino_temporada = None
        self.total_reservas = None
        self.puntaje = None

    def __repr__(self):
        return (f"Recomendacion(id={self.id}, nombre={self.nombre}, descripcion={self.descripcion}, "
                f"precio={self.precio}, destino_id={self.destino_id}, destino_nombre={self.destino_nombre}, "
                f"destino_temporada={self.destino_temporada}, total_reservas={self.total_reservas}, "
                f"puntaje={self.puntaje})")