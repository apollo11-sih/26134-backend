from fastapi import APIRouter,Depends
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.models.domain import District


router = APIRouter(
    prefix="/districts",
    tags=["districts"]
)

@router.get('/')
def get_districts(db:Session = Depends(get_db)):
    districts = db.query(District).filter(
        District.is_active == True
    ).all() #returning all districts

    return districts
