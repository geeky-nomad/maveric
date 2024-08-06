"""
The web entrypoint to the application.
"""
from mav_framework.Application import app
from mav_services.partners.app.Routes.partners import router as product_router
from mav_structure.utilities.load_llm import load_model
from mav_structure.utilities.load_rag import load_rag

from mav_structure.models.common import Base

Base.create_tables()


@app.on_event("startup")
async def startup_event():
    load_rag()
    load_model()


@app.get("/health")
async def health():
    return {"status": "healthy"}


app.include_router(product_router)  # TODO -> bootstrap the application instance through a function
