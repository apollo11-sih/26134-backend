from app.database.session import SessionLocal
from app.models.domain import District

db = SessionLocal()
#adding example districts
districts = [
    District(name="Pune", state="Maharashtra"),
    District(name="Nashik", state="Maharashtra"),
    District(name="Mumbai", state="Maharashtra"),
    District(name="Nagpur", state="Maharashtra"),
]


db.add_all(districts)
db.commit()
db.close()

print("Districts added successfully :D")