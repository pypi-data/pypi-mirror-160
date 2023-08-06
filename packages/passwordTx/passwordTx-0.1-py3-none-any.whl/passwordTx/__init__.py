import os

from .transaction import PasswordTx

ROOT_DIR = os.path.join(os.path.expanduser('~'), ".password_tx")
os.makedirs(ROOT_DIR, exist_ok=True)