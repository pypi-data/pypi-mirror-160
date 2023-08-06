import base64
import getpass
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from passwordTx import ROOT_DIR


def create_key(password:str):
    """ create fernet key from password
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"\xa1\xce'\xfe\xd6\x9d\x80\xd0/\xe9\n\x11\x12\xe8'\x91",
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))


def encrypt_key(username: str, key: str, private_key: str):
    """ encrypt & save privateKey to ROOT_DIR
    """
    fernet = Fernet(key)
    with open(os.path.join(ROOT_DIR, username), "wb") as f:
        f.write(fernet.encrypt(private_key.encode('utf-8')))


def decrypt_key(key: str, username: str):
    """ read & decrpyt privateKey from ROOT_DIR
    """
    fernet = Fernet(key)
    with open(os.path.join(ROOT_DIR, username), "rb") as f:
        return fernet.decrypt(f.read()).decode('utf-8')


def read_private_key(username: str):
    """ read private key with password
    """
    password = getpass.getpass("PASSWORD :")
    try:
        key = create_key(password)
        return decrypt_key(key, username)
    except Exception as e:
        raise ValueError("WRONG PASSWORD")