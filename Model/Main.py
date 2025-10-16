import os
import sys
from dotenv import load_dotenv
from domain.account import Usuario

if __package__ in (None, ""):
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def main() -> None:
    load_dotenv()
    print(opciones())

if __name__ == "__main__":
    main()