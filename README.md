# sqlalchemy-nest

[![PyPI - Version](https://img.shields.io/pypi/v/sqlalchemy-nest)](https://pypi.org/project/sqlalchemy-nest/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sqlalchemy-nest)](https://pypi.org/project/sqlalchemy-nest/)
[![Downloads](https://static.pepy.tech/badge/sqlalchemy-nest)](https://pepy.tech/project/sqlalchemy-nest)
[![CI](https://github.com/satorudev976/sqlalchemy-nest/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/satorudev976/sqlalchemy-nest/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/satorudev976/sqlalchemy-nest/graph/badge.svg?token=67ESOOAA5E)](https://codecov.io/gh/satorudev976/sqlalchemy-nest)

sqlalchemy-nest is easy create nested models for sqlalchemy

### Installation

```
pip install sqlalchemy-nest
```

### Create Nested Model

1. Set declarative_base constructor

    use ```declarative_nested_model_constructor``` for declarative_base constructor

    ```python
    from sqlalchemy import Column, ForeignKey, Integer, String
    from sqlalchemy.orm import declarative_base, relationship
    from sqlalchemy_nest import declarative_nested_model_constructor

    Base = declarative_base(constructor=declarative_nested_model_constructor)

    class Root(Base):
        __tablename__ = "root"
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(100))
        
        branches = relationship("Branch", back_populates="root", uselist=True, lazy="joined")
        
    class Branch(Base):
        __tablename__ = "branch"
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(100))
        root_id = Column(Integer, ForeignKey("root.id"))
        
        root = relationship("Root")
    ```

1. Initialization from **kwargs
    
    sets attributes on the constructed instance using the names and values in kwargs.

    ```python
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
    Root(id=1, name='root', branches=[Branch(id=1, name='branch', root_id=1)])
    ```

### Merge Nested Model

1. Set declarative_base constructor and cls

    use ```declarative_nested_model_constructor```  and ```BaseModel``` for declarative_base
    
    ⚠ sqlalchemy-nest checks viewonly to decide whether to update or not, so please set the viewonly property in the relationship. ⚠

    ```python
    from sqlalchemy import Column, ForeignKey, Integer, String
    from sqlalchemy.orm import declarative_base, relationship
    from sqlalchemy_nest import declarative_nested_model_constructor
    from sqlalchemy_nest.orm import BaseModel

    Base = declarative_base(cls=BaseModel, constructor=declarative_nested_model_constructor)

    class Root(Base):
        __tablename__ = "root"
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(100))
        
        branches = relationship("Branch", back_populates="root", uselist=True, lazy="joined")
        
    class Branch(Base):
        __tablename__ = "branch"
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(100))
        root_id = Column(Integer, ForeignKey("root.id"))
        
        root = relationship("Root", viewonly=True)
    ```

1. Update from **kwargs

    
    ```python
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
    Root(id=1, name='root', branches=[Branch(id=1, name='branch', root_id=1)])

    update_root = {
        'id': 1,
        'name': 'updated_root',
        'branches': [
            {
                'id': 1,
                'name': 'updated_branch',
            },
            {
                'name': 'created_branch',
            },
        ] 
    }
    >>> added_root.merge(**update_root)
    >>> session.commit()
    >>> updated_root: Root = session.query(Root).filter(Root.id == 1).first()
    Root(id=1, name='updated_root', branches=[Branch(id=1, name='updated_branch', root_id=1), Branch(id=2, name='created_branch', root_id=1)])    
    ```
