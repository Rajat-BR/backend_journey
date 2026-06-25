from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordBearer
from exceptions.custom_exceptions import InvalidTokenError


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


#JWT Configurations
SECRET_KEY = "d7028625d8a2e26f2512a14bc40dd391fadab6214d86a15c171efae841958e4a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        **data,
        "exp": expire
    }
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )   

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise InvalidTokenError("Invalid Token !")


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)
    