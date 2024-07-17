from fastapi.responses import JSONResponse
from mav_structure.Repositories.Partners.products import get_products


async def products():
    # fetch the associated repo for the products
    return JSONResponse(get_products())
