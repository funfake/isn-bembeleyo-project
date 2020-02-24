from passlib.context import CryptContext

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def encrypt_password(password):
    return pwd_context.encrypt(password)

def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)

monpass = "salut"
monautrepass = "hey"
monpass_crypt = encrypt_password(monpass)

print(monpass)
print(monpass_crypt)

print(check_encrypted_password(monautrepass, monpass_crypt)) # password à vérifier, password déjà hashé :: return True or False