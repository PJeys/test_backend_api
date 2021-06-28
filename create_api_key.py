import secrets

print("input length of API Key")
length = int(input())
generated_key = secrets.token_urlsafe(length-1)
print(generated_key)
