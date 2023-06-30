import hashlib

text = "0123456789"

hash = hashlib.sha512(str(text).encode('utf-8')).hexdigest()
print(hash)