from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.mineral import MiningStatus, DataQualityFlag


class MineralBase(BaseModel):
    mineral_name: str
    region_province: str
    category: str
    primary_use_industry: str
    applications: str
    mining_status: MiningStatus
    year_recorded: int
    source_system: str
    is_verified: bool = False
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    data_quality_flag: DataQualityFlag


class MineralCreate(MineralBase):
    pass


class MineralUpdate(BaseModel):
    mineral_name: Optional[str] = None
    region_province: Optional[str] = None
    category: Optional[str] = None
    primary_use_industry: Optional[str] = None
    applications: Optional[str] = None
    mining_status: Optional[MiningStatus] = None
    year_recorded: Optional[int] = None
    source_system: Optional[str] = None
    is_verified: Optional[bool] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0) # Pydantic will reject any value outside 0.0-1.0 automatically
    data_quality_flag: Optional[DataQualityFlag] = None


class MineralResponse(MineralBase):
    model_config = ConfigDict(from_attributes=True) # lets Pydantic read directly from SQLAlchemy model

    record_id: UUID
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    is_active: bool
    deleted_at: Optional[datetime] = None