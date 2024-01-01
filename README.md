# sqlalchemy-nest

sqlalchemy-nest is easy create nested models for sqlalchemy

# Getting started

models.py
```python

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
```

```

root = {
    'name': 'root',
    'branches': [
        {
            'name': 'branch',
        },
    ] 
}
>>> session.add(Root(**root))
>>> session.commit()
>>> added_root: Root = session.query(Root).filter(Root.id == 1).first()
Root(id=1, name='root', branches=[Branch(id=1, name='branch')])
```
