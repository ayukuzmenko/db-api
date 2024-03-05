from db_api.schemas.base import BaseSchema


class HealthSchema(BaseSchema):
    status: str
    message: str
