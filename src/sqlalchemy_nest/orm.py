from typing import Any
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.properties import RelationshipProperty


class BaseModel(object):
    """Base class used for declarative_base.

    The :class:`BaseModel` can updating of nested models from keywords
    This class should set to sqlalchemy `declarative_base` as base class like this:
    .. code-block:: python

        from sqlalchemy.orm import declarative_base

        from sqlalchemy_nest import declarative_nested_model_constructor
        from sqlalchemy_nest.orm import BaseModel

        Base = declarative_base(cls=BaseModel, constructor=declarative_nested_model_constructor)

        class MyTable(Base):
            __tablename__ = "my_table"
    """

    def merge(self, **kwargs: Any) -> None:
        self._merge(**kwargs)

    def _merge(self, parent=None, **kwargs: Any) -> None:
        for column in class_mapper(type(self)).columns:
            if not column.foreign_keys and not column.primary_key:
                setattr(self, column.key, kwargs.get(column.key))

        for composite in class_mapper(type(self)).composites:
            value = kwargs.get(composite.key)
            if value:
                setattr(self, composite.key, composite.composite_class(**value))

        for relationship in class_mapper(type(self)).relationships:
            if parent and type(parent) == relationship.mapper.entity:
                continue

            value = kwargs.get(relationship.key)
            if isinstance(value, list) or isinstance(getattr(self, relationship.key), list):
                if value:
                    self._merge_one_to_many_relationship(relationship, value)
                else:
                    setattr(self, relationship.key, [])
            else:
                if value:
                    self._merge_one_to_one_relationship(relationship, value)
                else:
                    setattr(self, relationship.key, None)

    def _merge_one_to_one_relationship(self, relationship: RelationshipProperty[Any], value: dict[str, Any]):
        relationship_entity: BaseModel = getattr(self, relationship.key)
        if relationship_entity:
            relationship_entity._merge(parent=self, **value)
        else:
            setattr(self, relationship.key, relationship.mapper.entity(**value))

    def _merge_one_to_many_relationship(self, relationship: RelationshipProperty[Any], values: list[dict[str, Any]]):
        relationship_entities: list[BaseModel] = getattr(self, relationship.key)
        pks = relationship.entity.primary_key

        for entity in relationship_entities:
            if all(getattr(entity, pk.name) != elem.get(pk.name) for pk in pks for elem in values):
                relationship_entities.remove(entity)

        for entity in relationship_entities:
            for elem in values:
                if all(getattr(entity, pk.name) == elem.get(pk.name) for pk in pks):
                    entity._merge(parent=self, **elem)

        for elem in values:
            if all(elem.get(pk.name) is None for pk in pks):
                relationship_entities.append(relationship.mapper.entity(**elem))
