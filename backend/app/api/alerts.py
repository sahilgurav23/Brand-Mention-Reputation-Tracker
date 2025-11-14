"""
Alerts API endpoints
"""
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.database import Alert, AlertConfig, get_db
from app.models.schemas import AlertCreate, AlertResponse, AlertConfigCreate, AlertConfigResponse
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.get("", response_model=List[AlertResponse])
async def list_alerts(
    db: Session = Depends(get_db),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    alert_type: Optional[str] = Query(None, description="Filter by alert type"),
    limit: int = Query(50, description="Number of records to return"),
):
    """
    List alerts with optional filters
    """
    query = db.query(Alert)

    if is_active is not None:
        query = query.filter(Alert.is_active == (1 if is_active else 0))
    if alert_type:
        query = query.filter(Alert.alert_type == alert_type)

    alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()

    logger.info(f"Retrieved {len(alerts)} alerts")
    return alerts


@router.post("", response_model=AlertResponse)
async def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new alert
    """
    try:
        db_alert = Alert(
            alert_type=alert.alert_type,
            title=alert.title,
            description=alert.description,
            severity=alert.severity,
        )

        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)

        logger.info(f"Created alert {db_alert.id}")
        return db_alert

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating alert: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific alert by ID
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    return alert


@router.put("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    """
    Mark an alert as resolved
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_active = 0
    alert.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(alert)

    logger.info(f"Resolved alert {alert_id}")
    return alert


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete an alert
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db.delete(alert)
    db.commit()

    logger.info(f"Deleted alert {alert_id}")
    return {"message": "Alert deleted successfully"}


# Alert Configuration endpoints


@router.get("/config", response_model=List[AlertConfigResponse])
async def list_alert_configs(
    db: Session = Depends(get_db),
):
    """
    List alert configurations
    """
    configs = db.query(AlertConfig).all()
    logger.info(f"Retrieved {len(configs)} alert configs")
    return configs


@router.post("/config", response_model=AlertConfigResponse)
async def create_alert_config(
    config: AlertConfigCreate,
    db: Session = Depends(get_db),
):
    """
    Create alert configuration
    """
    try:
        db_config = AlertConfig(
            name=config.name,
            alert_type=config.alert_type,
            threshold=config.threshold,
            window_hours=config.window_hours,
        )

        db.add(db_config)
        db.commit()
        db.refresh(db_config)

        logger.info(f"Created alert config {db_config.id}")
        return db_config

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating alert config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config/{config_id}", response_model=AlertConfigResponse)
async def get_alert_config(
    config_id: int,
    db: Session = Depends(get_db),
):
    """
    Get alert configuration
    """
    config = db.query(AlertConfig).filter(AlertConfig.id == config_id).first()

    if not config:
        raise HTTPException(status_code=404, detail="Alert config not found")

    return config


@router.put("/config/{config_id}", response_model=AlertConfigResponse)
async def update_alert_config(
    config_id: int,
    config_update: AlertConfigCreate,
    db: Session = Depends(get_db),
):
    """
    Update alert configuration
    """
    config = db.query(AlertConfig).filter(AlertConfig.id == config_id).first()

    if not config:
        raise HTTPException(status_code=404, detail="Alert config not found")

    config.name = config_update.name
    config.alert_type = config_update.alert_type
    config.threshold = config_update.threshold
    config.window_hours = config_update.window_hours

    db.commit()
    db.refresh(config)

    logger.info(f"Updated alert config {config_id}")
    return config


@router.delete("/config/{config_id}")
async def delete_alert_config(
    config_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete alert configuration
    """
    config = db.query(AlertConfig).filter(AlertConfig.id == config_id).first()

    if not config:
        raise HTTPException(status_code=404, detail="Alert config not found")

    db.delete(config)
    db.commit()

    logger.info(f"Deleted alert config {config_id}")
    return {"message": "Alert config deleted successfully"}
