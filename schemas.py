"""
Database Schemas for ChatImmo Rebuild

Each Pydantic model represents a MongoDB collection (lowercased class name).
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Lead(BaseModel):
    full_name: str = Field(..., description="Lead full name")
    email: EmailStr = Field(..., description="Lead email address")
    phone: Optional[str] = Field(None, description="Phone number")
    company: Optional[str] = Field(None, description="Company or agency")
    message: Optional[str] = Field(None, description="Context or goal")
    source: str = Field("website", description="Acquisition source")

class ContactMessage(BaseModel):
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    subject: str = Field(..., description="Message subject")
    message: str = Field(..., description="Message content")

class Subscriber(BaseModel):
    email: EmailStr = Field(..., description="Subscriber email")
    source: str = Field("newsletter", description="Subscription source")

# Backward-compatible examples kept for reference (not used by app)
class User(BaseModel):
    name: str
    email: EmailStr
    address: Optional[str] = None
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
