"""
The web entrypoint to the application.
"""
from mav_framework.Application import app
from mav_services.partners.app.Routes.partners import router as product_router

from mav_structure.models.common import Base

Base.create_tables()

app.include_router(product_router)  # TODO -> bootstrap the application instance through a function
