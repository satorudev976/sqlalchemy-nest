# sqlalchemy-nest example

example using sqlalchemy-nest based on the fastapi tutorial

https://fastapi.tiangolo.com/tutorial/sql-databases/

There is no PUT API in fastapi tutorial, so implement PUT API

The difference will be as follows

### Use sqlalchemy-nest Base class

```database.py```

```diff
+ from sqlalchemy_nest import declarative_nested_model_constructor
+ from sqlalchemy_nest.orm import BaseModel

...

- Base = declarative_base()
+ Base = declarative_base(cls=BaseModel, constructor=declarative_nested_model_constructor)
```

### Add cascade (If Need)

The delete-orphan cascade can also be applied to a many-to-one or one-to-one relationship, so that when an object is de-associated from its parent, it is also automatically marked for deletion.

```models.py```

```diff
- items = relationship("Item", back_populates="owner")
+ items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")
```

### Add nested model

Create nested model so that Item can be created when creating User

```schemas.py```

```diff
class UserCreate(UserBase):
    password: str
+   items: list[ItemCreate] = []

+  class UserUpdate(UserBase):
+      is_active: bool = True
+      items: list[ItemUpdate] = []
```


### Create/Update from **kwargs

```crud.py```

```diff
def create_user(db: Session, user: schemas.UserCreate):
-    fake_hashed_password = user.password + "notreallyhashed"
-    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
+    db_user = models.User(**user.model_dump())


-　def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
-     db_item = models.Item(**item.dict(), owner_id=user_id)
-     db.add(db_item)
-     db.commit()
-     db.refresh(db_item)
-     return db_item
+  def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
+      db_user: models.User = get_user(db, user_id)
+      db_user.merge(**user.model_dump())
+      db.commit()
+      db.refresh(db_user)
+      return db_user
```

### Implement PUT API

```main.py```

```diff
+  @app.put("/users/{user_id}", response_model=schemas.User)
+  def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
+      return crud.update_user(db=db, user_id=user_id, user=user)
```


If you run it with Uvicorn:

```
pip install --no-cache-dir --upgrade -r requirements.txt

uvicorn sql_app.main:app --reload
```

And then, you can open your browser at http://127.0.0.1:8000/docs.
