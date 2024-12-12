from sqlalchemy import Column, UUID, Float, DateTime, ForeignKey
from app.models.base import BaseModel
import uuid

class Prediction(BaseModel):
    __tablename__ = "predictions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    index_id = Column(UUID(as_uuid=True), ForeignKey("indices.id"), nullable=False)
    target_date = Column(DateTime, nullable=False)
    predicted_price = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False) 