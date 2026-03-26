import enum
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class MiningStatus(enum.Enum):
    Active = "Active"
    Inactive = "Inactive"
    Artisanal = "Artisanal"

class DataQualityFlag(enum.Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    FIELD_ESTIMATE = "FIELD_ESTIMATE"
    CONFLICTING_SOURCE = "CONFLICTING_SOURCE"
    AWAITING_REVIEW = "AWAITING_REVIEW"

class Mineral(Base):
    __tablename__ = "minerals"

    record_id = Column(UUID(as_uuid=True), primary_key=True)
    mineral_name = Column(String, nullable=False)
    region_province = Column(String, nullable=False)
    category = Column(String, nullable=False)
    primary_use_industry = Column(String, nullable=False)
    applications = Column(Text, nullable=False)
    mining_status = Column(Enum(MiningStatus), nullable=False)
    year_recorded = Column(Integer, nullable=False)
    source_system = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(String, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    confidence_score = Column(Float, nullable=False)
    data_quality_flag = Column(Enum(DataQualityFlag), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    deleted_at = Column(DateTime, nullable=True)