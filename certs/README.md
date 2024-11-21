# Создание приватного ключа
```bash
openssl genrsa -out jwt-private.pem 2048
```

# Создание публичного ключа на основе приватного
```bash
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```