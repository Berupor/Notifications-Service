import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse, JSONResponse
import backoff

from api.v1 import events
from core.config import settings

from message_broker.rabbitmq.rabbitmq_broker import get_rabbitmq
from fastapi.exceptions import RequestValidationError
from api.v1.utls.decorators import exception_handler
from core import exceptions

app = FastAPI(
    title="API для получения и обработки нотификаций пользователя",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
@backoff.on_exception(
    backoff.expo,
    (ConnectionError),
    max_time=1000,
    max_tries=10,
)
async def startup():

    rabbitmq = get_rabbitmq()
    await rabbitmq.connect()


@app.on_event("shutdown")
async def shutdown():
    rabbitmq = get_rabbitmq()
    await rabbitmq.close()


@app.exception_handler(RequestValidationError)
@exception_handler
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom error message for pydantic error
    """
    # Get the original 'detail' list of errors
    error = exc.errors()[0]
    raise exceptions.BadRequestException(extra_information=error["msg"])


app.include_router(events.router, prefix="/api/v1/notification", tags=["Notifications"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.fastapi.host, port=settings.fastapi.port, reload=True
    )
