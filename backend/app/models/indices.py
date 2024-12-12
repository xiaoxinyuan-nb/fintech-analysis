from sqlalchemy import Column, String, UUID, Text
from app.models.base import BaseModel
import uuid

class Index(BaseModel):
    __tablename__ = "indices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(32), unique=True, index=True, nullable=False)
    name = Column(String(64), nullable=False)
    description = Column(Text) 