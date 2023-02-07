import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import events
from core.config import settings
from message_broker.rabbitmq.rabbitmq_broker import get_rabbitmq

app = FastAPI(
    title="API для получения и обработки нотификаций пользователя",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    rabbitmq = get_rabbitmq()
    await rabbitmq.connect()


@app.on_event("shutdown")
async def shutdown():
    rabbitmq = get_rabbitmq()
    await rabbitmq.close()


app.include_router(events.router, prefix="/api/v1/notification", tags=["Notifications"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.fastapi.host, port=settings.fastapi.port, reload=True
    )
