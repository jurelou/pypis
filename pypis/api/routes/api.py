from fastapi import APIRouter

from pypis.api.routes import legacy

router = APIRouter()


@router.get("/ping")
def ping():
    return "Magneto api version: "


router.include_router(legacy.router, tags=["legacy", "simple"], prefix="/simple")
