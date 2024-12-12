from sqlalchemy import Column, UUID, Float, DateTime, ForeignKey
from app.models.base import BaseModel
import uuid

class RealtimeQuote(BaseModel):
    __tablename__ = "realtime_quotes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    index_id = Column(UUID(as_uuid=True), ForeignKey("indices.id"), nullable=False)
    price = Column(Float, nullable=False)
    change = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

class KlineData(BaseModel):
    __tablename__ = "kline_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    index_id = Column(UUID(as_uuid=True), ForeignKey("indices.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False) 