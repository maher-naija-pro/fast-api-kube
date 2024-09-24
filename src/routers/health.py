from fastapi import APIRouter


router= APIRouter(prefix='')


@router.get("/health", response_model=dict)
def health_check():
    return {"status": "healthy"}
