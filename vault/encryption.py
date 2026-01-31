import cryptography
from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.PASSWORD_ENCRYPTION_KEY)

def encrypt_pass(plain_password:str)->str:
    encrypted = fernet.encrypt(plain_password.encode())
    return encrypted.decode()

def decrypt_pass(encrypted_password:str)->str:
    encrypted = fernet.decrypt(encrypted_password.encode())
    return encrypted.decode()
