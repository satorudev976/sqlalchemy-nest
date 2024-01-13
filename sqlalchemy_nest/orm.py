from typing import Any
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.properties import RelationshipProperty


class BaseModel(object):
    
    def merge(self, **kwargs: Any) -> None:
        for column in class_mapper(type(self)).columns:
            if not column.foreign_keys and not column.primary_key:
                setattr(self, column.key, kwargs.get(column.key))
        
        for composite in class_mapper(type(self)).composites:
            if kwargs.get(composite.key):
                setattr(self, composite.key, composite.composite_class(**kwargs.get(composite.key)))
        
        for relationship in class_mapper(type(self)).relationships:
            if relationship.viewonly:
                continue
            
            if isinstance(kwargs.get(relationship.key), list) or isinstance(getattr(self, relationship.key), list):
                if kwargs.get(relationship.key):
                    self._merge_one_to_many_relationship(relationship, kwargs.get(relationship.key))
                else:
                    setattr(self, relationship.key, [])
            else:
                if kwargs.get(relationship.key):
                    self._merge_one_to_one_relationship(relationship, kwargs.get(relationship.key))
                else:
                    setattr(self, relationship.key, None)

    def _merge_one_to_one_relationship(self, relationship: RelationshipProperty[Any], value):
        relationship_cls = getattr(self, relationship.key)
        if relationship_cls:
            relationship_cls.merge(**value)
        else:
            setattr(self, relationship.key, relationship.mapper.entity(**value))

    def _merge_one_to_many_relationship(self, relationship: RelationshipProperty[Any], values):
        relationship_cls = getattr(self, relationship.key)
        pks = relationship.entity.primary_key
        should_remove_entities = relationship_cls[:]
        for elem in values:
            if all(elem.get(pk.name) is None for pk in pks):
                relationship_cls.append(relationship.mapper.entity(**elem))
                continue
            
            for entity in relationship_cls:
                if all(getattr(entity, pk.name) == elem.get(pk.name) for pk in pks):
                    entity.merge(**elem)
                    should_remove_entities.remove(entity)

        for should_remove_entity in should_remove_entities:
            relationship_cls.remove(should_remove_entity)
