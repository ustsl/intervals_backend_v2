from sqlalchemy import Boolean, Column, DateTime, func


class MaintenanceModel:

    __abstract__ = True

    is_active = Column(Boolean(), default=True, nullable=False)
    is_deleted = Column(Boolean(), default=False, nullable=False)


class TimeModel:

    __abstract__ = True

    time_create = Column(DateTime(timezone=True), default=func.now())
    time_update = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
