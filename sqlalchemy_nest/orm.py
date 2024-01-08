from typing import Any
from sqlalchemy.orm import class_mapper


class BaseModel(object):
    
    def update(self, **kwargs: Any) -> None:
        for column in class_mapper(type(self)).columns:
            if not column.foreign_keys and not column.primary_key:
                setattr(self, column.key, kwargs.get(column.key))
        
        for composite in class_mapper(type(self)).composites:
            if kwargs.get(composite.key):
                setattr(self, composite.key, composite.composite_class(**kwargs[composite.key]))
        
        for relationship in class_mapper(type(self)).relationships:
            if relationship.viewonly:
                continue
            if kwargs.get(relationship.key):
                relationship_cls = getattr(self, relationship.key)
                if isinstance(kwargs.get(relationship.key), list):
                    pks = relationship.entity.primary_key
                    should_remove_entities = relationship_cls.copy()
                    
                    for elem in kwargs.get(relationship.key):
                        if all(elem.get(pk.name) is not None for pk in pks):
                            for entity in relationship_cls:
                                if all(getattr(entity, pk.name) == elem.get(pk.name) for pk in pks):
                                    entity.update(**elem)
                                    should_remove_entities.remove(entity)
                        else:
                            relationship_cls.append(relationship.mapper.entity(**elem))
                    
                    for should_remove_entity in should_remove_entities:
                        relationship_cls.remove(should_remove_entity)
                            
                if isinstance(kwargs.get(relationship.key), dict):
                    if relationship_cls:
                        relationship_cls.update(**kwargs.get(relationship.key))
                    else:
                        setattr(self, relationship.key, relationship.mapper.entity(**kwargs[relationship.key]))
            else:
                self.remove_relationship(relationship)
    
    def remove_relationship(self, relationship):
        if isinstance(getattr(self, relationship.key), list):
            setattr(self, relationship.key, [])
        else:
            setattr(self, relationship.key, None)
