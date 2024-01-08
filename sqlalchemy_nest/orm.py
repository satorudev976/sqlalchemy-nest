from typing import Any
from sqlalchemy.orm import class_mapper

class BaseModel(object):
    
    def update(self: Any, **kwargs: Any) -> None:
        cls_ = type(self)
        columns = class_mapper(cls_).columns
        relationships = class_mapper(cls_).relationships
        composites = class_mapper(cls_).composites
        
        for column in columns:
            if column.foreign_keys or column.primary_key:
                continue
            else:
                setattr(self, column.key, kwargs.get(column.key))
        
        for composite in composites:
            if kwargs.get(composite.key): 
                setattr(self, composite.key, composite.composite_class(**kwargs[composite.key]))
        
        for relationship in relationships:
            if relationship.viewonly:
                continue
            if kwargs.get(relationship.key):
                if isinstance(kwargs.get(relationship.key), list):
                    relationship_clses = getattr(self, relationship.key)
                    pks = class_mapper(relationship.mapper.entity).primary_key
                    should_remove_entities = relationship_clses.copy()
                    
                    for elem in kwargs.get(relationship.key):
                        if all(elem.get(pk.name) is not None for pk in pks):
                            for relationship_cls in relationship_clses:
                                if all(getattr(relationship_cls, pk.name) == elem.get(pk.name) for pk in pks):
                                    relationship_cls.update(**elem)
                                    should_remove_entities.remove(relationship_cls)
                        else:
                            relationship_clses.append(relationship.mapper.entity(**elem))
                    
                    for should_remove_entity in should_remove_entities:
                        relationship_clses.remove(should_remove_entity)
                            
                if isinstance(kwargs.get(relationship.key), dict):
                    relationship_cls = getattr(self, relationship.key)
                    if relationship_cls:
                        relationship_cls.update(**kwargs.get(relationship.key))
                    else:
                      setattr(self, relationship.key, relationship.mapper.entity(**kwargs[relationship.key]))  
            else:
                if getattr(self, relationship.key) and isinstance(getattr(self, relationship.key), list):
                    setattr(self, relationship.key, [])
                else:    
                    setattr(self, relationship.key, kwargs.get(relationship.key))
