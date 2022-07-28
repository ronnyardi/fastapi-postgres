from uuid import uuid4
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, default=lambda: str(uuid4()), index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    address = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    vulns = relationship("Vuln", back_populates="reporter")


class Vuln(Base):
    __tablename__ = "vulns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    reporter_id = Column(Integer, ForeignKey("users.id"))

    reporter = relationship("User", back_populates="vulns")
