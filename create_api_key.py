import secrets

length = 16
generated_key = secrets.token_urlsafe(length)
print(generated_key)
