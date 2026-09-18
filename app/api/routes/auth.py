from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest #requesting email + password
from app.database.session import get_db #gives endpoint access to postgresql 
from app.models.domain import User
from app.core.security import verify_password,create_access_token #checks password against hash


router = APIRouter(prefix="/auth",tags=['authentication'])

@router.post('/login')
def login(login_data:LoginRequest,db:Session =Depends(get_db)):
    #searching for email to match in database
    user = db.query(User).filter(User.email == login_data.email).first() 

    #no matching email id
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email ID or password :("
        )

    #password not matching to email id
    if not verify_password(login_data.password,user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email ID or password :("
        )

    access_token = create_access_token(
        user_id=user.id,
        role=user.role    
    )

    #finally returning if everything goes correctly
    return {
        "login_status" : "Login Successful :D",
        "access_token" : access_token,
        "token_type": "bearer",
        "user" : user.id,
        "role": user.role
    }