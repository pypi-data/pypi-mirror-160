from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get(
    "/is-healthy",
    description="web app health checking",
    response_class=PlainTextResponse)
async def health_check():
    return "🆗"
