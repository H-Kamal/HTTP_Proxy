from sqlalchemy import Boolean, Column, String

from .database import Base


class URL_Look_Up(Base):
    __tablename__ = "URL Look Up"

    url = Column(String, primary_key=True, index=True)
    allowed = Column(Boolean, default=True)