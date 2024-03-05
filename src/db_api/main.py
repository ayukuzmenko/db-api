from fastapi import FastAPI

from db_api.api.crud_routes import router as crud_router
from db_api.api.transaction_routes import router as transaction_router
from db_api.schemas.health_schema import HealthSchema

app = FastAPI(title="DB Application", openapi_url="/api/v1/openapi.json")


@app.get("/health")
async def health_check() -> HealthSchema:
    return HealthSchema(status="Ok", message="Service is up and running.")


app.include_router(crud_router, prefix="/api")
app.include_router(transaction_router, prefix="/api")
