# Importamos lo necesario desde nuestros archivos
from app import app, db
from models import User # Asegúrate que tu archivo models.py define la clase User

print("Intentando crear las tablas de la base de datos...")

# Necesitamos el 'contexto' de la aplicación para que SQLAlchemy sepa
# a qué base de datos conectarse (la configurada en app.config)
with app.app_context():
    # El comando mágico que crea las tablas definidas en models.py
    db.create_all()

print("¡Listo! Las tablas deberían haberse creado en site.db si no hubo errores.")