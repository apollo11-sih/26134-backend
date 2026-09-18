from pwdlib import PasswordHash
from app.core.config import get_settings
from datetime import datetime,timedelta,timezone
import jwt

settings = get_settings()


#password hasher using Argon2(default hai)
password_hash = PasswordHash.recommended()

def create_access_token(user_id:int,role:str) ->str:
    #creating a expiry token time
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "id":str(user_id),
        "role":role,
        "exp":expire
    }
    return jwt.encode(payload,settings.SECRET_KEY,algorithm=settings.ALGORITHM)


def hash_password(password: str) -> str:
    #convert the plain password into a secure hash
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    #check whether the entered password matches the stored hash
    return password_hash.verify(password, hashed_password)