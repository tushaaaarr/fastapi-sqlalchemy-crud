import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import database as _database


class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    is_active = _sql.Column(_sql.Boolean, default=True)
    addresses = _orm.relationship("Address", back_populates="owner")


class Address(_database.Base):
    __tablename__ = "addresses"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    address = _sql.Column(_sql.String, index=True)
    coordinates = _sql.Column(_sql.String, index=True,default='')
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    owner = _orm.relationship("User", back_populates="addresses")