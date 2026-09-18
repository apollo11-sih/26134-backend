from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.domain import Company
from app.schemas.company import CompanyCreate, CompanyResponse


router = APIRouter(
    prefix="/companies",
    tags=["companies"]
)

#creating a new company
@router.post("/", response_model=CompanyResponse)
def create_company(company_data: CompanyCreate, db: Session = Depends(get_db)
):
    # creating new company using the data sent by the frontend
    company = Company(
        name=company_data.name,
        sector_id=company_data.sector_id
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return company

#getting all companies 
@router.get("/", response_model=list[CompanyResponse])
def get_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()

#getting single company
@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    #finding company using id
    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    #giving error if company not found 
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found :("
        )

    return company

#updating a company
@router.put('/{company_id}',response_model=CompanyResponse)
def update_company(company_id:int,company_data:CompanyCreate,db:Session = Depends(get_db)):
    #finding the company we want
    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    #stopping
    if not company:
        raise HTTPException(
            status_code=404,
            tags="Company not found"
        )

    #updating name and sector id
    company.name = company_data.name
    company.sector_id = company_data.sector_id

    db.commit()
    db.refresh(company)
    return company

@router.delete('/{company_id}')
def delete_company(company_id:int,db:Session = Depends(get_db)):
    #getting the company to delete
    company = db.query(Company).filter(
        Company.id == company.id
    ).first()

    #company not found
    if not company:
        raise HTTPException(
            status_code=404,
            tags="Company not found"
        )

    #if found then delete it hehehehehe :)
    db.delete(company)
    db.commit
    return {
        "message":"Company has been deleted from the database"
    }

