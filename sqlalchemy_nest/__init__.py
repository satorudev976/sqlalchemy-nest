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
    
    for k in kwargs:
        if not hasattr(cls_, k):
            continue
        
        if isinstance(kwargs[k], list):  # "one-to-many"
            relation_cls = relationships[k].mapper.entity
            for elem in kwargs[k]:
                if isinstance(elem, dict):
                    instances = [relation_cls(**elem) for elem in kwargs[k]]
                    setattr(self, k, instances)
                else:
                    setattr(self, k, kwargs[k])
        
        elif isinstance(kwargs[k], dict):  # "one-to-one"
            if k in relationships:
                relation_cls = relationships[k].mapper.entity
                instance = relation_cls(**kwargs[k])
                setattr(self, k, instance)
            if k in composites:
                composite_cls = composites[k].composite_class
                instance = composite_cls(**kwargs[k])
                setattr(self, k, instance)
        else:
            setattr(self, k, kwargs[k])
