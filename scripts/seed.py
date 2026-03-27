import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from uuid import UUID
from datetime import datetime
from app.db.session import SessionLocal
from app.models.mineral import Mineral, MiningStatus, DataQualityFlag


XLSX_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "drc_minerals_production.xlsx")


def parse_datetime(value):
    if pd.isna(value):
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def seed():
    db = SessionLocal()

    try:
        existing = db.query(Mineral).count()
        if existing > 0:
            print(f"Database already has {existing} records. Skipping seed.")
            return

        print("Reading xlsx file...")
        df = pd.read_excel(XLSX_PATH, sheet_name="minerals_dataset")

        print(f"Seeding {len(df)} records...")
        minerals = []

        for _, row in df.iterrows():
            mineral = Mineral(
                record_id=UUID(row["record_id"]),
                mineral_name=row["mineral_name"],
                region_province=row["region_province"],
                category=row["category"],
                primary_use_industry=row["primary_use_industry"],
                applications=row["applications"],
                mining_status=MiningStatus(row["mining_status"]),
                year_recorded=int(row["year_recorded"]),
                source_system=row["source_system"],
                created_at=parse_datetime(row["created_at"]),
                created_by=row["created_by"],
                updated_at=parse_datetime(row["updated_at"]),
                updated_by=row["updated_by"],
                is_verified=bool(row["is_verified"]),
                confidence_score=float(row["confidence_score"]),
                data_quality_flag=DataQualityFlag(row["data_quality_flag"]),
                is_active=bool(row["is_active"]),
                deleted_at=parse_datetime(row["deleted_at"]),
            )
            minerals.append(mineral)

        db.bulk_save_objects(minerals)
        db.commit()
        print(f"Successfully seeded {len(minerals)} records.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()