from typing import Any
from sqlalchemy.orm import class_mapper


def declarative_nested_model_constructor(self: Any, **kwargs: Any) -> None:
    """A nested model support constructor that allows initialization from kwargs.

    Sets attributes on the constructed instance using the names and
    values in ``kwargs``.

    attributes of the instance's class are allowed. These could be,
    for example, any mapped columns or relationships or composites.
    """
    cls_ = type(self)

    relationships = class_mapper(cls_).relationships
    composites = class_mapper(cls_).composites

    for key, value in kwargs.items():
        if not hasattr(cls_, key):
            continue

        if isinstance(value, list):  # "one-to-many"
            if all(isinstance(elem, dict) for elem in value):
                setattr(self, key, [relationships[key].mapper.entity(**elem) for elem in value])
            else:
                setattr(self, key, value)
        elif isinstance(value, dict):  # "one-to-one"
            if key in relationships:
                setattr(self, key, relationships[key].mapper.entity(**value))
            if key in composites:
                setattr(self, key, composites[key].composite_class(**value))
        else:
            setattr(self, key, value)
