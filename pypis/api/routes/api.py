from fastapi import APIRouter

from pypis.api.routes import legacy

router = APIRouter()


@router.get("/ping")
def ping() -> str:
    """Webserver ping."""
    return "pong"


router.include_router(legacy.router, tags=["legacy", "simple"], prefix="/simple")
