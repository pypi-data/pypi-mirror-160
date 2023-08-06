from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey)
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class ServicesGuide(BaseModel):
    """  Справочник"""

    __tablename__ = 'services_guide'
    __table_args__ = {"extend_existing": True}

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    services = relationship('Services', back_populates='services_guide', uselist=True)

    def __repr__(self):
        return self.name


class Services(BaseModel):
    """ Услуги """

    __tablename__ = 'services'
    __table_args__ = {"extend_existing": True}

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    payment_required = Column(Boolean, default=False)
    need_validation = Column(Boolean, default=True)
    services_guide_id = Column(Integer, ForeignKey('services_guide.id'), nullable=False)

    services_guide = relationship('ServicesGuide', back_populates='services', uselist=False)

    def __repr__(self):
        return self.name
