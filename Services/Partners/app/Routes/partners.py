from fastapi import APIRouter
from ..Controllers.PartnerProductController import products

router = APIRouter()

router.get('/products')(products)