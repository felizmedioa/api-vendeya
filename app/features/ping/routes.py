from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
@router.head("/ping")
async def ping():
    return {"status": "ok"}
