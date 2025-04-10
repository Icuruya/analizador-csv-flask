# --- Importaciones ---
from flask import Flask, render_template, url_for, flash, redirect, request # Base Flask imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required # Flask-Login imports
from flask_bcrypt import Bcrypt
import os # Para trabajar con rutas de archivos
from werkzeug.utils import secure_filename # Para asegurar nombres de archivo

# --- NO FORM OR MODEL IMPORTS HERE --- #

# --- Inicializar Extensiones (SIN la app todavía) ---
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# --- Crear la Aplicación ---
app = Flask(__name__)

# --- Configuraciones de la App ---
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'uploads' # Nombre de la carpeta que creaste
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# (Opcional) Asegurarse de que la carpeta exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- Conectar las Extensiones con la App ---
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# --- Importar Modelo y Definir User Loader ---
# Importamos User UNA SOLA VEZ aquí, después de inicializar 'db'
from models import User

@login_manager.user_loader
def load_user(user_id):
    # Esta función le dice a Flask-Login cómo cargar un usuario desde el ID.
    # Ahora 'User' es conocido porque lo importamos justo arriba.
    return User.query.get(int(user_id))

# --- Rutas ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Importamos EL FORMULARIO específico aquí DENTRO
    from forms import RegistrationForm
    # 'User' ya es conocido por la importación global de arriba

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password_hash=hashed_password) # 'User' está disponible
        db.session.add(user)
        db.session.commit()
        flash(f'¡Cuenta creada para {form.username.data}! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Registro', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Importamos EL FORMULARIO específico aquí DENTRO
    from forms import LoginForm
    # 'User' ya es conocido por la importación global de arriba

    # Si el usuario ya está autenticado, redirigirlo
    if current_user.is_authenticated:
         return redirect(url_for('index'))

    form = LoginForm() # 'LoginForm' está disponible por la importación local
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() # 'User' está disponible
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login incorrecto. Verifica usuario y contraseña.', 'danger')
    return render_template('login.html', title='Iniciar Sesión', form=form)

# ... (después de la función @app.route('/login')...)

# --- Ruta para Logout ---
@app.route('/logout')
def logout():
    logout_user() # Función de Flask-Login que borra la sesión del usuario
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('dashboard')) # Redirige a la página principal

# --- Ruta Protegida para el Dashboard ---
@app.route('/dashboard')
@login_required # Este decorador protege la ruta
def dashboard():
    # Solo se llegará aquí si el usuario ha iniciado sesión.
    # Si no, Flask-Login lo redirigirá automáticamente a la página de 'login'
    # (según lo configuramos en login_manager.login_view).
    return render_template('dashboard.html', title='Dashboard')

# --- Ruta para manejar la carga de CSV ---
@app.route('/upload_csv', methods=['POST']) # Solo acepta POST
@login_required # Requiere que el usuario haya iniciado sesión
def upload_csv():
    # 1. Verificar si el archivo está en la petición
    if 'archivo_csv' not in request.files:
        flash('No se encontró la parte del archivo en la solicitud.', 'danger')
        return redirect(url_for('dashboard'))

    file = request.files['archivo_csv'] # Obtiene el archivo

    # 2. Verificar si el usuario seleccionó un archivo
    if file.filename == '':
        flash('Ningún archivo seleccionado.', 'warning')
        return redirect(url_for('dashboard'))

    # 3. Si el archivo existe y tiene un nombre...
    if file:
        # 4. Asegurar el nombre del archivo (evita caracteres extraños o rutas maliciosas)
        filename = secure_filename(file.filename)

        # 5. (Opcional pero recomendado) Verificar extensión
        if not filename.lower().endswith('.csv'):
             flash('Solo se permiten archivos .csv', 'danger')
             return redirect(url_for('dashboard'))

        # 6. Construir la ruta completa para guardar
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            # 7. Guardar el archivo
            file.save(save_path)
            flash(f'Archivo "{filename}" subido exitosamente. ¡Listo para analizar!', 'success')
            # --- AQUÍ ES DONDE LLAMARÍAS A LA LÓGICA DE ANÁLISIS EN EL FUTURO ---
            # Por ejemplo: procesar_csv(save_path)
        except Exception as e:
            flash(f'Ocurrió un error al guardar el archivo: {e}', 'danger')

        return redirect(url_for('dashboard')) # Vuelve al dashboard después de intentar subir

    # Si algo salió mal antes (aunque las verificaciones iniciales deberían cubrir esto)
    flash('Ocurrió un error inesperado al subir el archivo.', 'danger')
    return redirect(url_for('dashboard'))

# --- Bloque if __name__ == '__main__' ---
if __name__ == '__main__':
    app.run(debug=True)