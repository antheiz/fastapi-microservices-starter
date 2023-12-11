from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    # def __init__(self, model: Type[ModelType], ) -> None:
    #     self._model = model
    def __init__(
        self,
        model: Type[ModelType],
        post_create: Optional[Callable[[Session, ModelType], None]] = None,
    ) -> None:
        self._model = model
        self.post_create = post_create

    def create(self, session: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = dict(obj_in)
        db_obj = self._model(**obj_in_data)
        session.add(db_obj)
        session.commit()

        if self.post_create:
            self.post_create(session, db_obj)

        return db_obj

    def get(self, session: Session, *args, **kwargs) -> Optional[ModelType]:
        result = session.execute(select(self._model).filter(*args).filter_by(**kwargs))
        return result.scalars().first()

    def update(
        self,
        session: Session,
        *,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        db_obj: Optional[ModelType] = None,
        **kwargs,
    ) -> Optional[ModelType]:
        db_obj = db_obj or self.get(session, **kwargs)
        if db_obj is not None:
            obj_data = db_obj.dict()
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)
            session.commit()
        return db_obj

    def delete(
        self, session: Session, *args, db_obj: Optional[ModelType] = None, **kwargs
    ) -> ModelType:
        db_obj = db_obj or self.get(session, *args, **kwargs)
        session.delete(db_obj)
        session.commit()
        return db_obj
