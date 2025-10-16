import os
import sys
from dotenv import load_dotenv

if __package__ in (None, ""):
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from domain.account import Usuario
from presentation.account_vm import CuentaViewModel
from ui.account_cli import CuentaCLIView
from data.firebase_service import FirebaseRealtimeService


def main():
    load_dotenv()
    print(bienvenida())

if __name__ == "__main__":
    main()