from datetime import date, datetime
from typing import List
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


# Association Table for Many-to-Many: ServiceTicket <-> Mechanic
ticket_mechanic = db.Table(
    'ticket_mechanic',
    db.metadata,
    db.Column('ticket_id', ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', ForeignKey('mechanics.id'))
)

class Customer(db.Model):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)


    tickets: Mapped[List["ServiceTicket"]] = relationship("ServiceTicket", back_populates="customer")
    


class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    service_description: Mapped[str] = mapped_column(db.String(500), nullable=False)
     

    customer: Mapped["Customer"] = relationship("Customer", back_populates="tickets")
    mechanics: Mapped[List["Mechanic"]] = relationship(
        "Mechanic",
        secondary=ticket_mechanic,
        back_populates="tickets"
    )


class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), unique=True, nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    
    
    tickets: Mapped[List["ServiceTicket"]] = relationship(
        "ServiceTicket",
        secondary=ticket_mechanic,
        back_populates="mechanics"
    )


class InventoryItem(db.Model):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)


