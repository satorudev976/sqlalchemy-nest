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
    
    mapped_columns = class_mapper(cls_).columns
    relationships = class_mapper(cls_).relationships
    composites = class_mapper(cls_).composites
    
    for k in kwargs:
        if not hasattr(cls_, k):
            continue
        if k in mapped_columns:
            setattr(self, k, kwargs[k])
            continue
        elif k in relationships: 
            relation_cls = relationships[k].mapper.entity
            if isinstance(kwargs[k], list): # "one-to-many"
                for elem in kwargs[k]:
                    if isinstance(elem, dict):
                        instances = [relation_cls(**elem) for elem in kwargs[k]]
                        setattr(self, k, instances)
                    else:
                        setattr(self, k, kwargs[k])
            elif isinstance(kwargs[k], dict): # "one-to-one"
                instance = relation_cls(**kwargs[k])
                setattr(self, k, instance)
            else:
                setattr(self, k, kwargs[k])
        elif k in composites:
            if isinstance(kwargs[k], dict):
                composite_cls = composites[k].composite_class
                instance = composite_cls(**kwargs[k])
                setattr(self, k, instance)
            else:
                setattr(self, k, kwargs[k])