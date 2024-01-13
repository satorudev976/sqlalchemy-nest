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
    
    for k, v in kwargs.items():
        if not hasattr(cls_, k):
            continue
        
        if isinstance(v, list):  # "one-to-many"
            if all(isinstance(elem, dict) for elem in v):
                setattr(self, k, [relationships[k].mapper.entity(**elem) for elem in v])
            else:
                setattr(self, k, v)
        elif isinstance(v, dict):  # "one-to-one"
            if k in relationships:
                setattr(self, k, relationships[k].mapper.entity(**v))
            if k in composites:
                setattr(self, k, composites[k].composite_class(**v))
        else:
            setattr(self, k, v)
