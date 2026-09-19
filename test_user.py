from app.database.session import SessionLocal
from app.models.domain import User
from app.core.security import hash_password


#open a connection to the postgresql database
db = SessionLocal()

#test shit
user = User(
    name="Government Admin",
    phone_no="676767676769",
    email="123",
    password=hash_password("123"),
    role="government"
)

# adding the user to postgrsql
db.add(user)
db.commit()
db.close()

print("Government user created successfully :D")