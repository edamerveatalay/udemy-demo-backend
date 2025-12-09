import json
from fastapi import HTTPException, Header


def load_db():
    with open("app/mock/db.json", "r") as f:
        return json.load(f)


def create_fake_token(user_id: int):
    """
    Kullanıcı giriş yaptığında oluşturulan basit demo token.
    Örn: token-1
    """
    return f"token-{user_id}"


def decode_token(token: str):
    """
    Gelen token 'token-2' formatında olmalı.
    """
    if not token or not token.startswith("token-"):
        raise HTTPException(status_code=401, detail="Geçersiz token")

    try:
        user_id = int(token.split("-")[1])
        return user_id
    except:
        raise HTTPException(status_code=401, detail="Token çözülemedi")


def get_current_user(authorization: str = Header(None)):
    """
    Hem Swagger'ın gönderdiği:
        Authorization: Bearer token-1

    Hem kendi gönderdiğimiz:
        Authorization: token-1

    ikisini de destekler.
    """

    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header eksik")

    if authorization.startswith("Bearer "):
        authorization = authorization.replace("Bearer ", "").strip()

    user_id = decode_token(authorization)
    db = load_db()

    for user in db["users"]:
        if user["id"] == user_id:
            return user

    raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")


def require_role(required_role: str):
    """
    Role kontrolü yapan decorator fonksiyon.
    """

    def role_checker(user):
        if user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Bu işlem için yetkiniz yok")

    return role_checker
