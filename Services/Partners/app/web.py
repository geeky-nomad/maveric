"""
The web entrypoint to the application.
"""

from mav_framework.Application import app
from .Routes.partners import router as product_router

app.include_router(product_router)  # TODO -> bootstrap the application instance through a function
