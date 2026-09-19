from pydantic import BaseModel

#while creating a new company
class CompanyCreate(BaseModel):
    name:str
    sector_id:int | None = None

#returning a company from database
class CompanyResponse(BaseModel):
    id:int
    name:str
    sector_id:int
    model_config = {"from_attributes":True}