from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action_type = Column(String) # "BALANCO", "DRE", "INDICADORES", "SWING_TRADE"
    data = Column(JSON) # The actual content saved
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", backref="history")
