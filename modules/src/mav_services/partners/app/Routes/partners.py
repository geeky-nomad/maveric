from fastapi import APIRouter
from ..Controllers.PartnerProductController import products, partner_chatbot_entry, welcome, seed, select_category, \
    select_sub_category, chit_chat

router = APIRouter()

router.post('/welcome')(welcome)
router.post('/select-category')(select_category)
router.post('/select-sub-category')(select_sub_category)
router.post('/query')(chit_chat)
# ====================================================================
router.get('/products')(products)
router.get('/seed')(seed)
router.get('/chatbot')(partner_chatbot_entry)
