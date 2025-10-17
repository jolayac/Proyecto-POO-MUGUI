import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Model.usuario import Usuario
from View.ui import UsuarioView
from ViewModel.usuario_vm import UsuarioViewModel

load_dotenv()   # Carga las variables del archivo .env

def main():
    vm = UsuarioViewModel()
    View = UsuarioView(vm)
    View.run()

if __name__ == "__main__":
    main()