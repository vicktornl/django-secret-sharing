import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from django_secret_sharing.utils import (
    encrypt_value,
    transform_value_to_valid_block_length,
)

key = os.urandom(32)
iv = os.urandom(16)
value, value_length = transform_value_to_valid_block_length(b"test")

# print(value)
# print(value.__class__)
#
# print(value.encode("utf-8"))
# print(value.encode("utf-8").__class__)

cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

encryptor = cipher.encryptor()
ct = encryptor.update(value) + encryptor.finalize()

print(ct)

decryptor = cipher.decryptor()
dt = decryptor.update(ct) + decryptor.finalize()

print(dt[:value_length])
