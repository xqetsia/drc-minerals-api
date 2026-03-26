from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from app.models.mineral import Mineral
from app.schemas.mineral import MineralCreate, MineralUpdate


def get_minerals(
    db: Session,
    region: Optional[str] = None,
    category: Optional[str] = None,
    year: Optional[int] = None,
    mining_status: Optional[str] = None,
    is_verified: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(Mineral).filter(Mineral.is_active == True)

    #ilike => searching "kasai" matches "kasai-Oriental"
    if region:
        query = query.filter(Mineral.region_province.ilike(f"%{region}%"))
    if category:
        query = query.filter(Mineral.category.ilike(f"%{category}%"))
    if year:
        query = query.filter(Mineral.year_recorded == year)
    if mining_status:
        query = query.filter(Mineral.mining_status == mining_status)
    if is_verified is not None:
        query = query.filter(Mineral.is_verified == is_verified)

    return query.offset(skip).limit(limit).all()


def get_mineral_by_id(db: Session, record_id: UUID):
    return db.query(Mineral).filter(
        Mineral.record_id == record_id,
        Mineral.is_active == True
    ).first()


def create_mineral(db: Session, payload: MineralCreate, created_by: str = "api_user"):
    mineral = Mineral(
        record_id=uuid4(),
        **payload.model_dump(),
        created_at=datetime.utcnow(),
        created_by=created_by,
        updated_at=datetime.utcnow(),
        updated_by=created_by,
        is_active=True,
    )
    db.add(mineral)
    db.commit()
    db.refresh(mineral)
    return mineral


def update_mineral(db: Session, record_id: UUID, payload: MineralUpdate, updated_by: str = "api_user"):
    mineral = get_mineral_by_id(db, record_id)
    if not mineral:
        return None
    updates = payload.model_dump(exclude_unset=True)  # only fields the client actually sent get updated, everything else is left untouched
    for field, value in updates.items():
        setattr(mineral, field, value)
    mineral.updated_at = datetime.utcnow()
    mineral.updated_by = updated_by
    db.commit()
    db.refresh(mineral)
    return mineral


def soft_delete_mineral(db: Session, record_id: UUID):
    mineral = get_mineral_by_id(db, record_id)
    if not mineral:
        return None
    mineral.is_active = False
    mineral.deleted_at = datetime.utcnow()
    db.commit()
    return mineral


def get_summary(db: Session):
    total = db.query(func.count(Mineral.record_id)).filter(Mineral.is_active == True).scalar()
    verified = db.query(func.count(Mineral.record_id)).filter(
        Mineral.is_active == True,
        Mineral.is_verified == True
    ).scalar()
    by_category = dict(
        db.query(Mineral.category, func.count(Mineral.record_id))
        .filter(Mineral.is_active == True)
        .group_by(Mineral.category)
        .all()
    )
    by_region = dict(
        db.query(Mineral.region_province, func.count(Mineral.record_id))
        .filter(Mineral.is_active == True)
        .group_by(Mineral.region_province)
        .all()
    )
    year_range = db.query(
        func.min(Mineral.year_recorded),
        func.max(Mineral.year_recorded)
    ).scalar_one_or_none()

    return {
        "total_active_records": total,
        "verified_records": verified,
        "by_category": by_category,
        "by_region": by_region,
        "year_range": {"min": year_range[0], "max": year_range[1]} if year_range else {}
    }