# --- Importaciones ---
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# Nota: Quitamos las importaciones de forms y models de aquí por ahora,
# las pondremos solo donde se necesiten (dentro de las rutas)
# from forms import RegistrationForm # <--- COMENTA o ELIMINA esta línea de aquí
# from models import User           # <--- COMENTA o ELIMINA esta línea de aquí

# --- Inicializar Extensiones (SIN la app todavía) ---
# Creamos las instancias de las extensiones globalmente
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# Configuramos login_manager aquí donde sea posible
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# --- Crear la Aplicación (Factory Pattern opcional, pero bueno para entender) ---
# Podríamos poner esto en una función, pero por ahora lo dejamos aquí
app = Flask(__name__) # Creamos la instancia de Flask

# --- Configuraciones de la App ---
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' # Usa tu propia clave
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Conectar las Extensiones con la App ---
# Ahora que 'app' está creada y configurada, la registramos en las extensiones
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    # Esta función le dice a Flask-Login cómo cargar un usuario desde el ID.
    return User.query.get(int(user_id))

# --- Rutas ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Importamos FORMULARIO y MODELO aquí DENTRO, donde se usan
    from forms import RegistrationForm
    from models import User

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'¡Cuenta creada para {form.username.data}! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Registro', form=form)


# --- Bloque if __name__ == '__main__' ---
if __name__ == '__main__':
    # Nota: NO necesitas volver a llamar a db.create_all() aquí.
    # Eso se hace una vez con el script create_db.py o flask shell.
    app.run(debug=True)