from fastapi.responses import JSONResponse
from mav_structure.Repositories.Partners.products import get_products, insert_chatbot_details, product_categories, \
    seed_the_database, get_selected_category_items, get_selected_category_products, get_chit_chat
from mav_structure.schemas.partners import PartnerChatbotProfileResponse, WelcomeRequestSchema, CategorySchema, \
    SubCategorySchema, ChitChatSchema


async def welcome(schema: WelcomeRequestSchema):
    # repo call
    # TODO -> manage this conversation for each user through schema.user_id.
    _product_options = await product_categories()
    return JSONResponse({
        'message': 'Welcome to Hiketron chatbot, How can I assist you today?',
        'type': 'select-category',
        'options': _product_options
    })


async def select_category(schema: CategorySchema):
    selected_category = schema.selected_category
    selected_items = await get_selected_category_items(selected_category)
    return JSONResponse({
        'message': f'What kind of {selected_category.lower()} are you looking for?',
        'type': 'select-sub-category',
        'options': selected_items
    })


async def select_sub_category(schema: SubCategorySchema):
    selected_category = schema.selected_category
    selected_sub_category = schema.selected_sub_category
    _products = await get_selected_category_products(selected_sub_category)
    return JSONResponse({
        'message': 'Here is the matching product.',
        'type': 'checkout',
        'options': _products
    })


async def chit_chat(schema: ChitChatSchema):
    query = schema.query
    response = await get_chit_chat(query)
    if response.get('chit_chat'):
        return JSONResponse({
            'message': response.get('chit_chat').get('message'),
            'type': 'chit-chat',
            'options': []
        })
    elif response.get('category'):
        return JSONResponse({
            'message': 'Please select from the list',
            'type': 'select-sub-category',
            'options': response.get('category')
        })
    else:
        return JSONResponse({
            'message': 'Here are the matching products.',
            'type': 'select-sub-category',
            'options': response.get('sub_category')
        })


async def products():
    # fetch the associated repo for the products
    _handles = await get_products()
    return JSONResponse(_handles)


async def partner_chatbot_entry(schema: PartnerChatbotProfileResponse):
    _db_entry = await insert_chatbot_details(schema)
    response = PartnerChatbotProfileResponse.model_validate(_db_entry)
    return JSONResponse(content=response.model_dump())


# ----------------------- For DataEngineer and AI point of view ------------------------

async def seed():
    db_seed = await seed_the_database()
    if db_seed:
        return JSONResponse({'message': 'success'})
    return JSONResponse({'message': 'got an error while seeding the database'})
