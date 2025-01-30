from flask import session, render_template , request
from app.models.Actividad import Actividad
from app.models.db import db
from app.models.Usuario import Usuario
from app.models.Reserva import Reserva
from app.models.Destino import Destino
from sqlalchemy import func,text
from datetime import datetime
from app.FactoryRecomendacion.RecomendacionBasicaFactory import RecomendacionBasicaFactory
from app.FactoryRecomendacion.RecomendacionPremiumFactory import RecomendacionPremiumFactory
from app.controllers.RecomendacionService import RecomendacionService

from flask import session, render_template, request

def recomendaciones_basicas():
    usuario_id = session.get('user_id')
    if not usuario_id:
        return "Usuario no autenticado."

    fecha_inicial = request.form.get('fecha_inicial')
    fecha_final = request.form.get('fecha_final')

    fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%d") if fecha_inicial else datetime.strptime('2000-01-01', "%Y-%m-%d")
    fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d") if fecha_final else datetime.strptime('2025-12-31', "%Y-%m-%d")

    actividades = Actividad.query.all()

    usuario = Usuario.query.get(usuario_id)
    if 'cultura' in usuario.preferencias.lower(): 
        factory = RecomendacionPremiumFactory()
    else:
        factory = RecomendacionBasicaFactory()

    servicio = RecomendacionService(factory)

    recomendaciones = servicio.generar_recomendaciones(usuario_id, actividades, fecha_inicial, fecha_final)
    return render_template('recomendaciones_basicas.html', recomendaciones=recomendaciones)
    
def reportes():
    reservas_por_temporada = (
        db.session.query(
            Reserva.actividad_id,
            Destino.temporada_recomendada,
            func.count(Reserva.id).label("total_reservas")
        )
        .join(Actividad, Reserva.actividad_id == Actividad.id)
        .join(Destino, Actividad.destino_id == Destino.id)
        .group_by(Reserva.actividad_id, Destino.temporada_recomendada)
        .all()
    )
    
    reporte = {}
    for actividad_id, temporada, total_reservas in reservas_por_temporada:
        if temporada not in reporte:
            reporte[temporada] = []
        actividad = Actividad.query.get(actividad_id)
        reporte[temporada].append({
            "nombre": actividad.nombre,
            "descripcion": actividad.descripcion,
            "total_reservas": total_reservas
        })
    preferencias_totales = {}
    usuarios = Usuario.query.all()
    for usuario in usuarios:
        preferencias = usuario.preferencias.split(",") if usuario.preferencias else []
        for preferencia in preferencias:
            if preferencia not in preferencias_totales:
                preferencias_totales[preferencia] = 0
            preferencias_totales[preferencia] += 1

    preferencias_ordenadas = sorted(preferencias_totales.items(),key=lambda x: x[1],reverse=True)
    return render_template('reportes.html', reporte=reporte,preferencias_ordenadas=preferencias_ordenadas)
