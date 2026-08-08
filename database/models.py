from sqlalchemy import(
    column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    BigInteger
) 
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .postgres import Base

class user(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name=Column(String(100),nullable=False)

    email=Column(String(150), unique=True, nullable=False, index=True)

    hashed_password=Column(String(255), nullable=False)

    created_at=Column(DateTime(timezone=True), server_default=func.now())

    documents = relationship(
        "Document",
        back_populates="owner",
        cascade="all, delete"
    )

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(
        String(255),
        nullable=False
    )

    stored_filename = Column(
        String(255),
        nullable=False,
        unique=True
    )

    file_type=Column(
        String(20),
        nullable=False
    )

    processing_status=Column(
        String(30),
        default="uploaded"
    )

    uploaded_by=Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    created_at=Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    owner=relationship(
        "User",
        back_populates="documents"
    )