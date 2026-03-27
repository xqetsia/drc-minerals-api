from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.db.session import get_db
from app.schemas.mineral import MineralCreate, MineralUpdate, MineralResponse
from app.services import mineral_service
from app.core.security import require_api_key

router = APIRouter()

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    return mineral_service.get_summary(db)


@router.get("/", response_model=list[MineralResponse])
def list_minerals(
    region: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    mining_status: Optional[str] = Query(None),
    is_verified: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return mineral_service.get_minerals(
        db, region, category, year, mining_status, is_verified, skip, limit
    )


@router.get("/{record_id}", response_model=MineralResponse)
def get_mineral(record_id: UUID, db: Session = Depends(get_db)):
    mineral = mineral_service.get_mineral_by_id(db, record_id)
    if not mineral:
        raise HTTPException(status_code=404, detail="Mineral not found")
    return mineral


@router.post("/", response_model=MineralResponse, status_code=201)
def create_mineral(payload: MineralCreate,
                   db: Session = Depends(get_db),
                   api_key: str = Depends(require_api_key)):

    return mineral_service.create_mineral(db, payload)


@router.patch("/{record_id}", response_model=MineralResponse)
def update_mineral(record_id: UUID,
                   payload: MineralUpdate,
                   db: Session = Depends(get_db),
                   api_key: str = Depends(require_api_key)):

    mineral = mineral_service.update_mineral(db, record_id, payload)
    if not mineral:
        raise HTTPException(status_code=404, detail="Mineral not found")
    return mineral


@router.delete("/{record_id}", status_code=204)
def delete_mineral(
        record_id: UUID,
        db: Session = Depends(get_db),
        api_key: str = Depends(require_api_key)):

    mineral = mineral_service.soft_delete_mineral(db, record_id)
    if not mineral:
        raise HTTPException(status_code=404, detail="Mineral not found")