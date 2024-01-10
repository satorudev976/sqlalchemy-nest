from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import composite, declarative_base, relationship
from sqlalchemy_nest import declarative_nested_model_constructor
from sqlalchemy_nest.orm import BaseModel

Base = declarative_base(cls=BaseModel, constructor=declarative_nested_model_constructor)


class Root(Base):
    __tablename__ = "root"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    
    branches = relationship("Branch", back_populates="root", uselist=True, lazy="joined", cascade="all, delete-orphan", order_by="Branch.id")
    

class Branch(Base):
    __tablename__ = "branch"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    root_id = Column(Integer, ForeignKey("root.id"))
    
    root = relationship("Root", viewonly=True)
    nodes = relationship("Node", back_populates="branch", uselist=True, lazy="joined", cascade="all, delete-orphan", order_by="Node.id")


class Node(Base):
    __tablename__ = "node"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    branch_id = Column(Integer, ForeignKey("branch.id"))
    
    branch = relationship("Branch", viewonly=True)
    leaves = relationship("Leaf", back_populates="node", uselist=True, lazy="joined", cascade="all, delete-orphan", order_by="Leaf.id")


class Leaf(Base):
    __tablename__ = "leaf"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    node_id = Column(Integer, ForeignKey("node.id"))
    
    node = relationship("Node", viewonly=True)


class DateRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __composite_values__(self):
        return self.start, self.end

    def __repr__(self):
        return f"DateRange(start={self.start!r}), end={self.end!r}"

    def __eq__(self, other):
        return isinstance(other, DateRange) and other.start == self.start and other.end == self.end

    def __ne__(self, other):
        return not self.__eq__(other)

class Reservation(Base):
    __tablename__ = "reservation"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    start_date = Column(Date)
    end_date = Column(Date)
    
    registration_card = relationship("RegistrationCard", back_populates="reservation", uselist=False, lazy="joined", cascade="all, delete-orphan")    
    date_range = composite(DateRange, start_date, end_date)


class RegistrationCard(Base):
    __tablename__ = "registration_card"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    guest_name = Column(String(100))
    reservation_id = Column(Integer, ForeignKey("reservation.id"), unique=True)
    
    reservation = relationship("Reservation", viewonly=True)