# firebase_authentication.py
import pyrebase
import requests
from typing import Optional, Dict

# Configuración de Firebase (reemplaza con tus datos reales)
firebase_config = {
    "apiKey": "AIzaSyCTI5_fE9Y-lOXu6aUSG23vZUD-19rwS1o",
    "authDomain": "proyecto-poo-mugui.firebaseapp.com",
    "databaseURL": "https://proyecto-poo-mugui-default-rtdb.firebaseio.com",
    "projectId": "proyecto-poo-mugui",
    "storageBucket": "proyecto-poo-mugui.firebasestorage.app",
    "messagingSenderId": "945352912383",
    "appId": "1:945352912383:web:299d8b1e90a2bb4b3f0bca",
    "measurementId": "G-490V0WW1N2"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

class FirebaseAuthentication:
    """Clase que maneja toda la comunicación con Firebase Authentication"""

    def __init__(self):
        self.current_user = None  # Guardará el usuario autenticado

    def sign_in_with_google(self, id_token: str) -> Dict:
        try:
            api_key = firebase_config["apiKey"]
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={api_key}"
            payload = {
                "postBody": f"id_token={id_token}&providerId=google.com",
                "requestUri": "http://localhost",
                "returnSecureToken": True,
                "returnIdpCredential": True
            }
            r = requests.post(url, json=payload)
            if r.ok:
                data = r.json()
                self.current_user = data
                return {"success": True, "user": data}
            else:
                return {"success": False, "error": r.text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_current_user(self) -> Optional[Dict]:
        """Devuelve el usuario actual si está logueado"""
        return self.current_user

    def sign_out(self):
        """Cierra sesión"""
        self.current_user = None