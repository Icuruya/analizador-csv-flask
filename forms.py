from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
# Importamos el modelo User para poder verificar si un usuario ya existe
from models import User

class RegistrationForm(FlaskForm):
    # Campo para el nombre de usuario
    username = StringField('Nombre de Usuario',
                           validators=[DataRequired(message="El nombre de usuario es obligatorio."),
                                       Length(min=4, max=25, message="Debe tener entre 4 y 25 caracteres.")])

    # Campo para la contraseña
    password = PasswordField('Contraseña',
                             validators=[DataRequired(message="La contraseña es obligatoria.")])

    # Campo para confirmar la contraseña
    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[DataRequired(message="Confirma la contraseña."),
                                                 EqualTo('password', message='Las contraseñas deben coincidir.')])

    # Botón de envío
    submit = SubmitField('Registrarse')

    # --- Validadores personalizados ---

    # WTForms busca métodos que empiecen con validate_<nombre_del_campo>
    # y los ejecuta automáticamente durante la validación.
    def validate_username(self, username):
        # Consultamos la base de datos para ver si ya existe un usuario con ese nombre.
        user = User.query.filter_by(username=username.data).first()
        if user:
            # Si user no es None, significa que ya existe, lanzamos un error de validación.
            raise ValidationError('Ese nombre de usuario ya está en uso. Por favor, elige otro.')
