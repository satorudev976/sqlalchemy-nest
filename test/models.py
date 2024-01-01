from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_nest import declarative_nested_model_constructor

Base = declarative_base(constructor=declarative_nested_model_constructor)


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
    
    root = relationship("Root")
    nodes = relationship("Node", back_populates="branch", uselist=True, lazy="joined", cascade="all, delete-orphan", order_by="Node.id")


class Node(Base):
    __tablename__ = "node"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    branch_id = Column(Integer, ForeignKey("branch.id"))
    
    branch = relationship("Branch")
    leaves = relationship("Leaf", back_populates="node", uselist=True, lazy="joined", cascade="all, delete-orphan", order_by="Leaf.id")


class Leaf(Base):
    __tablename__ = "leaf"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    node_id = Column(Integer, ForeignKey("node.id"))
    
    node = relationship("Node")