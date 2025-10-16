#FireBase admin
import firebase_admin
from firebase_admin import credentials, db
from usuario import Usuario

if __package__ in (None, ""):
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from domain.account import Usuario
from presentation.account_vm import CuentaViewModel
from ui.account_cli import CuentaCLIView
from data.firebase_service import FirebaseRealtimeService

cred = credenciales.Certificate('') # Ruta del archivo JSON
firebase_admin.initialize_app(cred, {'databaseURL': '' # URL de la base de datos
}) # Inicializa la aplicación de Firebase --- IGNORE ---
