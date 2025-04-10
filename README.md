# Analizador CSV con Flask (Demo Base)

## Resumen Ejecutivo

* **Descripción:** Aplicación web desarrollada con Python y el micro-framework Flask. Permite la gestión de usuarios (registro, inicio y cierre de sesión) y proporciona una base para la carga y futuro análisis de archivos CSV. Utiliza SQLAlchemy para la interacción con la base de datos y Flask-Login para la autenticación.
* **Problema Identificado:** Necesidad de una herramienta web centralizada para usuarios registrados que permita subir conjuntos de datos en formato CSV para su posterior procesamiento, análisis y visualización, evitando la gestión manual de archivos y accesos.
* **Solución Propuesta:** Esta aplicación ofrece un sistema de autenticación seguro y una interfaz para cargar archivos CSV. Establece la base para módulos futuros de análisis, visualización y exportación de datos. La versión actual demuestra el registro, login, logout, protección de rutas y carga de archivos.
* **Arquitectura:**
    * **Backend:** Python con Flask.
    * **Base de Datos:** SQLite (para desarrollo, fácilmente reemplazable por PostgreSQL/MySQL en producción).
    * **ORM:** Flask-SQLAlchemy.
    * **Autenticación:** Flask-Login para manejo de sesiones y protección de rutas.
    * **Formularios:** Flask-WTF para generación y validación segura de formularios.
    * **Contraseñas:** Flask-Bcrypt para hashing seguro de contraseñas.
    * **Plantillas:** Jinja2 (integrado en Flask) para renderizado de HTML.
    * **Frontend:** HTML5, CSS básico (integrado en plantillas).
    * **Servidor Desarrollo:** Servidor Werkzeug integrado en Flask (`flask run`).
    * **Servidor Producción (Recomendado):** WSGI (Gunicorn, uWSGI) + Web Server (Nginx, Apache).

## Tabla de Contenidos

* [Requerimientos](#requerimientos)
* [Instalación](#instalación)
* [Configuración](#configuración)
* [Uso](#uso)
* [Contribución](#contribución)
* [Roadmap](#roadmap)

## Requerimientos

* **Servidor Web/Aplicación:**
    * Desarrollo: Servidor de desarrollo Flask/Werkzeug (incluido).
    * Producción: Se recomienda un servidor WSGI como [Gunicorn](https://gunicorn.org/) o [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) detrás de un servidor web como [Nginx](https://nginx.org/) o [Apache](https://httpd.apache.org/).
* **Base de Datos:**
    * Desarrollo: SQLite (archivo `site.db`, creado automáticamente).
    * Producción: Se recomienda [PostgreSQL](https://www.postgresql.org/) o [MySQL](https://www.mysql.com/). La configuración se cambia en `app.config['SQLALCHEMY_DATABASE_URI']`.
* **Lenguaje:** [Python](https://www.python.org/) (v3.7 o superior recomendado).
* **Paquetes Adicionales (Python):** Ver archivo `requirements.txt`. Los principales son:
    * `Flask`
    * `Flask-SQLAlchemy`
    * `Flask-Login`
    * `Flask-Bcrypt`
    * `Flask-WTF`
    * `Werkzeug` (usado para `secure_filename`)

## Instalación

**1. Ambiente de Desarrollo:**

* **Clonar Repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/analizador-csv-flask.git](https://github.com/TU_USUARIO/analizador-csv-flask.git) # Reemplaza con tu URL
    cd analizador-csv-flask
    ```
* **Crear Entorno Virtual:**
    ```bash
    python -m venv venv
    ```
* **Activar Entorno Virtual:**
    * Windows PowerShell: `.\venv\Scripts\Activate.ps1` (puede requerir `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`)
    * Windows CMD: `.\venv\Scripts\activate.bat`
    * macOS / Linux: `source venv/bin/activate`
* **Instalar Dependencias:** (Asegúrate de que `venv` esté activo)
    ```bash
    pip install -r requirements.txt
    ```
* **Crear Base de Datos:** (Asegúrate de que `venv` esté activo)
    ```bash
    python create_db.py
    ```
* **Ejecutar Aplicación:** (Asegúrate de que `venv` esté activo)
    ```bash
    flask run
    ```
* Acceder en el navegador: `http://127.0.0.1:5000` (o la URL indicada).

**2. Pruebas Manuales:**

No hay un framework de pruebas automatizadas implementado aún. Las pruebas manuales consisten en:
* Navegar a la página principal.
* Registrar un nuevo usuario a través del formulario `/register`.
* Intentar registrar el mismo usuario de nuevo (debería fallar).
* Iniciar sesión con credenciales incorrectas (debería fallar).
* Iniciar sesión con credenciales correctas (`/login`).
* Verificar que la navegación cambia (muestra saludo, logout).
* Acceder al `/dashboard` (debería funcionar).
* Subir un archivo no-CSV (debería fallar).
* Subir un archivo CSV válido (debería mostrar éxito y el archivo aparecer en la carpeta `/uploads`).
* Intentar acceder a `/dashboard` después de cerrar sesión (`/logout`) (debería redirigir a `/login`).

**3. Implementación en Producción (Ejemplo Básico - Local con Gunicorn):**

* Asegúrate de que `gunicorn` esté instalado (`pip install gunicorn`).
* Asegúrate de que `debug=True` esté **desactivado** en `app.run()` dentro de `app.py` (o elimínalo, ya que `flask run` no se usa).
* Configura variables de entorno para `SECRET_KEY` y `SQLALCHEMY_DATABASE_URI` (apuntando a tu BD de producción).
* Ejecuta desde la terminal (con `venv` activo):
    ```bash
    gunicorn --workers 3 --bind 0.0.0.0:8000 app:app
    ```
    (Ajusta workers y bind según necesidad. `app:app` se refiere al objeto `app` dentro del archivo `app.py`).
* Accede a través de `http://<tu_ip>:8000`. Se recomienda usar Nginx o Apache como proxy inverso delante de Gunicorn.

**4. Implementación en Producción (Ejemplo Básico - Heroku):**

* Instala [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
* Asegúrate de que `gunicorn` está en `requirements.txt`.
* Crea un archivo `Procfile` (sin extensión) en la raíz del proyecto con el contenido:
    ```Procfile
    web: gunicorn app:app
    ```
* Inicia sesión en Heroku: `heroku login`.
* Crea una app en Heroku: `heroku create nombre-de-tu-app` (o deja que genere uno).
* Configura una base de datos (ej. Heroku Postgres): `heroku addons:create heroku-postgresql:hobby-dev`. Heroku pondrá la URL en una variable de entorno `DATABASE_URL`.
* Adapta `app.py` para leer `DATABASE_URL` del entorno si existe, y asegúrate de cambiar `sqlite:///` por `postgresql:///` o similar si usas la variable de Heroku. *Nota: SQLAlchemy > 1.4 requiere `postgresql+psycopg2`*. Necesitarás `psycopg2-binary` en `requirements.txt`.
* Configura la `SECRET_KEY` como variable de entorno en Heroku: `heroku config:set SECRET_KEY='tu_clave_secreta_muy_larga'`.
* Añade `Procfile` a git: `git add Procfile`, `git commit -m "Add Procfile"`.
* Despliega: `git push heroku main` (o `master`).
* Ejecuta las migraciones/creación de BD en Heroku si es necesario (ej. `heroku run python create_db.py` - **¡CUIDADO!** `create_db.py` borraría tablas existentes si ya existen; para producción real se usan herramientas de migración como Flask-Migrate/Alembic).

## Configuración

* **Configuración del Producto:**
    * Las configuraciones principales se encuentran en `app.py` bajo la sección `app.config[...]`.
    * `SECRET_KEY`: Clave secreta para sesiones y seguridad de formularios. **Debe cambiarse y mantenerse secreta en producción** (idealmente usando variables de entorno).
    * `SQLALCHEMY_DATABASE_URI`: Cadena de conexión a la base de datos. Para producción, cambiar a la URI de PostgreSQL/MySQL y obtenerla de variables de entorno.
    * `UPLOAD_FOLDER`: Carpeta donde se guardan los archivos CSV subidos.
* **Configuración de Requerimientos:**
    * Las dependencias exactas de Python están fijadas en `requirements.txt`. Instalar con `pip install -r requirements.txt`.

## Uso

**Referencia para Usuario Final:**

1.  **Acceso:** Abre tu navegador y ve a la URL de la aplicación (ej. `http://127.0.0.1:5000`).
2.  **Registro:** Si eres un usuario nuevo, haz clic en "Registrarse". Completa el formulario con un nombre de usuario único y una contraseña. Haz clic en "Registrarse". Serás redirigido a la página principal.
3.  **Inicio de Sesión:** Haz clic en "Iniciar Sesión". Ingresa tu nombre de usuario y contraseña. Puedes marcar "Recuérdame" para mantener la sesión activa por más tiempo. Haz clic en "Iniciar Sesión". Serás redirigido al Dashboard.
4.  **Dashboard:** Una vez iniciada la sesión, puedes acceder al Dashboard. Aquí encontrarás la opción para cargar archivos CSV.
5.  **Cargar CSV:** En el Dashboard, haz clic en "Seleccionar archivo", elige un archivo `.csv` de tu computadora y haz clic en "Subir y Analizar (Próximamente)". Recibirás un mensaje de confirmación.
6.  **Cerrar Sesión:** Haz clic en "Cerrar Sesión" en la barra de navegación para terminar tu sesión.

**Referencia para Usuario Administrador:**

*Actualmente, no hay funcionalidades específicas implementadas para roles de administrador.* Un administrador necesitaría interactuar directamente con la base de datos `site.db` (o la base de datos de producción) para gestionar usuarios por ahora.

## Contribución

¡Las contribuciones son bienvenidas! Sigue estos pasos:

1.  **Haz un Fork** del repositorio en GitHub.
2.  **Clona tu Fork** a tu máquina local:
    ```bash
    git clone [https://github.com/TU_USUARIO/analizador-csv-flask.git](https://github.com/TU_USUARIO/analizador-csv-flask.git)
    cd analizador-csv-flask
    ```
3.  **Crea una Nueva Rama** para tu característica o corrección:
    ```bash
    git checkout -b feature/MiNuevaCaracteristica # O fix/MiCorreccion
    ```
4.  **Realiza tus Cambios:** Escribe tu código, añade pruebas si es posible.
5.  **Haz Commit** de tus cambios:
    ```bash
    git add .
    git commit -m "Añadir MiNuevaCaracteristica"
    ```
6.  **Sube tus Cambios** a tu Fork en GitHub:
    ```bash
    git push origin feature/MiNuevaCaracteristica
    ```
7.  **Abre un Pull Request (PR):** Ve a tu Fork en GitHub y haz clic en "Compare & pull request". Describe tus cambios y envía el PR al repositorio original.
8.  **Espera la Revisión:** Espera comentarios o la aprobación y merge de tu PR.

## Roadmap (Futuras Características)

* **Roles de Usuario:** Implementar roles (ej. Administrador, Usuario) con diferentes permisos.
* **Gestión de Usuarios (Admin):** Panel para que administradores puedan ver/editar/eliminar usuarios.
* **Análisis de CSV:** Procesar el archivo CSV subido usando `pandas` para leer, validar y limpiar datos.
* **Almacenamiento de Datos CSV:** Guardar los datos procesados del CSV en la base de datos (posiblemente en nuevas tablas).
* **Visualización de Datos:** Generar gráficos (barras, líneas, pastel) a partir de los datos del CSV usando librerías como `Plotly` (Python/JS) o `Chart.js` (JS).
* **Tabla Dinámica:** Mostrar datos importantes del CSV en una tabla interactiva (usando DataTables.js).
* **Filtrado/Consultas:** Permitir al usuario filtrar o hacer consultas sobre los datos cargados.
* **Exportación de Datos:** Permitir descargar los datos procesados o los gráficos generados (ej. como CSV, PNG).
* **Interfaz de Usuario Mejorada:** Usar un framework CSS como Bootstrap o Tailwind para mejorar la apariencia.
* **(Avanzado) Consultas en Lenguaje Natural (NLP):** Implementar un módulo para interpretar solicitudes del usuario en lenguaje natural sobre los datos.
* **Pruebas Automatizadas:** Añadir pruebas unitarias y de integración (ej. con `pytest`).
* **Gestión de Perfil:** Permitir a los usuarios cambiar su contraseña.