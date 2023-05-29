from passlib.context import CryptContext
# A module used to encryp password using passlib, each encryption is a "hashing" which means the original password can't be obtained from the cipher text, verification can only be done by comparing two cipher text
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], default="pbkdf2_sha256", pbkdf2_sha256__default_rounds=30000)  # Initialise the passlib encryption module with default setting

# Takes in a value and returned the hashed one


def encrypt_password(password):
    return pwd_context.hash(password)

# Compare two encrypted value


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)
