from typing import List
import fastapi as _fastapi
import schemas as _schemas
from fastapi import Depends
from models import User,Address
app = _fastapi.FastAPI()
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas
import math 
import geopy.distance


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_address(address_id: int,db: Session = Depends(get_db)):
    return db.query(Address).filter(Address.id == address_id).first()

# Users Section
@app.get("/view-all_users", response_model=List[schemas.User])
def view_user(db: Session = Depends(get_db)):
    records =db.query(User).all()
    if not records is None:
        return records
    else:
        return {"message": f"No User found...."}


@app.post("/add-user/", response_model=_schemas.User)
def create_user(
    user: _schemas.UserCreate, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="User already exists"
        )
    else:
        fake_hashed_password = user.password
        db_user = User(email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

# Address Section

# Retrive all Addresses
@app.get("/user/{user_id}/view-addresses/", response_model=List[schemas.Address])
def view_addresses(user_id:int, db: Session = Depends(get_db)):
    records =db.query(Address).filter(Address.owner_id == user_id).all()
    return records

# Retrive one address
@app.get("/user/view-address/{address_id}", response_model=schemas.Address)
def view_address(address_id:int, db: Session = Depends(get_db)):
    records = db.query(Address).filter(Address.id == address_id).first()
    if not records is None:
        return records
    else:
        return {"message": f"No User found...."}

# Create new address
@app.post("/user/{user_id}/create-addresse/", response_model=_schemas.Address)
def create_address(user_id: int,address: _schemas.AddressCreate,db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise _fastapi.HTTPException(   
            status_code=404, detail="user does not exist"
        )
    else:
        address_dict = {
            "address": address.dict().get('address'),           
            "coordinates": address.dict().get('coordinates')
        }
        address = Address(**address_dict, owner_id=user_id)
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

# Update Existing Address
@app.patch("/user/update-address/{address_id}", response_model=schemas.Address)
def update_add(address_id: int,address: _schemas.AddressCreate,db: Session = Depends(get_db)):
    db_address = get_address(db=db, address_id=address_id)
    if not db_address is None:
        db_address.address = address.address
        address_coordinates = address.dict().get('coordinates')
        db_address.coordinates = address_coordinates
        db.commit()
        db.refresh(db_address)
        return db_address
    else:
        return {"message": f"Address Not found for this ID: {address_id}"}

# Delete Address
@app.delete("/user/delete-addresse/{address_id}")
def delete_address(address_id: int,db: Session = Depends(get_db)):
    db_address = get_address(db=db, address_id=address_id)
    if not db_address is None:
        db.query(Address).filter(Address.id == address_id).delete()
        
        return {"message": f"successfully deleted address with id: {address_id}"}
    else:
        return {"message": f"Address Not found for this ID: {address_id}"}

# Retrive addresses within a given distance and address(coordinates)
@app.post("/user/retrive-my_locations")
def update_add(address: _schemas.AddressWithDistance,db: Session = Depends(get_db)):
    records =db.query(Address).all()
    given_dist =address.dict()['distance']
    # Point one
    lon1 = float(address.dict()['coordinates'].split(',')[1].split(':')[1])
    lat1 = float(address.dict()['coordinates'].split(',')[0].split(':')[1])
    loc_list = []
    for i in records:
        # Point two 
        lon2 = float(i.coordinates.split(',')[1].split(':')[1])
        lat2 = float(i.coordinates.split(',')[0].split(':')[1])

        coords_1 = (lon1, lat1)
        coords_2 = (lon2, lat2)
        # distance in km
        loc_dist = geopy.distance.geodesic(coords_1, coords_2).km
        # check if address within given distance
        if loc_dist <= given_dist:
            locaction_dict = {
                'Address':i.address,
                'Distance':loc_dist
            }
            loc_list.append(locaction_dict)
    return loc_list
