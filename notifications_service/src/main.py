import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings

app = FastAPI(
    title="API для получения и обработки нотификаций пользователя",
    version="1.0.0",
    docs_url="/ugc/api/openapi",
    openapi_url="/ugc/api/openapi.json",
    default_response_class=ORJSONResponse,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.fastapi.host, port=settings.fastapi.port, reload=True
    )
