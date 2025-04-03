from app import db, login_manager # Importamos db y login_manager desde app.py
from flask_login import UserMixin # Necesario para Flask-Login


# Esta función es requerida por Flask-Login.
# Le dice cómo cargar un usuario dado su ID (que se guarda en la sesión).
#@login_manager.user_loader
#def load_user(user_id):
    # Convierte el user_id (que es string por defecto) a int y busca en la BD
    #return User.query.get(int(user_id))

# Nuestra clase User. Hereda de db.Model (para SQLAlchemy) y UserMixin (para Flask-Login)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # Llave primaria
    username = db.Column(db.String(50), unique=True, nullable=False) # Usuario único, no nulo
    # Guardaremos el hash bcrypt (es más largo que SHA256)
    password_hash = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='USER') # Rol, por defecto 'USER'

    # Cómo se representará el objeto User cuando lo imprimamos (útil para debug)
    def __repr__(self):
        return f"User('{self.username}', '{self.role}')"

    # Flask-Login usa la propiedad 'id' por defecto, así que no necesitamos definir get_id()
    # si nuestra llave primaria se llama 'id'.

    # Añadiremos métodos para verificar la contraseña aquí después.