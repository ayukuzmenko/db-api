from db_api.schemas.base import BaseSchema


class ItemSchema(BaseSchema):
    id: int
    value: str


class ItemCreateSchema(BaseSchema):
    value: str
