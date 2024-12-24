from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algorithm
# Expriation time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # payload > {'user_id': 1, 'exp': 1679915153}
        id: str = payload.get("user_id")
        # id > 1
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        # token_data > id='1'    
    
    except JWTError:
        raise credentials_exception

    return token_data



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # token > eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2Nzk5MTUxNTN9.Ej1l5hiO1A8VUDuvtdTyfDPPY6FWm3GYwLTX3lnPNqQ
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    # token > id='1'
    user = db.query(models.User).filter(models.User.id == token.id).first()
    # burdaki user postgredeki bir row
    # user.__dict__ > {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x7fae4b413490>, 'email': 'user@example.com', 'created_at': datetime.datetime(2023, 3, 27, 12, 34, 49, 902983, tzinfo=datetime.timezone.utc), 'id': 1, 'password': '$2b$12$KmZ6ZWvx00qa2T0/w71PyOJFVK8bu7f4sLvQltk57zIvpjOKDIcHq'}

    return user

