import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from datetime import datetime, timedelta
import numpy as np
from mav_structure.models.partners import PartnerChatbotProfile, Customer, SalesTransaction, Store, Product, Partner
from mav_framework.database.blueprint import use_db_session
import pandas as pd
from faker import Faker
import uuid
from enum import Enum
from mav_structure.NLP.product_search import extract_entities

# ----
from mav_structure.utilities.load_llm import generate_chit_chat_response
from mav_structure.utilities.load_classifier import classify_intent
from mav_structure.utilities.load_rag import handle_user_query

# Faker instance
faker = Faker()

csv_path = 'mav_structure/Data/hiketron.csv'
df = pd.read_csv(csv_path)


class IntentEnum(Enum):
    CHITCHAT = "Chit-chat"
    PRODUCTSEARCH = "PRODUCTSEARCH"


async def get_products():
    # Get the current script's director
    return df['Handle'].unique().tolist()


async def product_categories() -> list:
    response_text = [
        "Show me Liquid soap dispensers",
        "Show me Laundry Detergent",
        "Show me Skin Care",
        "Show me Hair Care",
        "Explore our Gift Card section"
    ]
    response_value = [
        'Liquid Soap Dispensers',
        'Laundry Detergent',
        'Skin Care',
        'Hair Care',
        'Gift Card'
    ]
    product_mapping = list(map(lambda x, y: {'text': x, 'value': y}, response_text, response_value))
    return product_mapping


async def get_selected_category_items(category):
    category = df[df['Type'] == category]['Title'].tolist()
    # convert category in the format {'text': '', 'value': ''}
    mapping_categories = [{'text': ' '.join(word.capitalize() for word in _item.split('-')), 'value': _item} for _item
                          in category]
    return mapping_categories


async def get_selected_category_products(sub_category):
    product_list = []
    df_filtered = df[df['Title'] == sub_category]
    df_selected = df_filtered[['Handle', 'Variant Price', 'Image Src', 'Product URL']]
    products = df_selected.to_dict(orient='records')
    final_di = dict(
        title=products[0].get('Handle'),
        variant_price=products[0].get('Variant Price'),
        image_src=products[0].get('Image Src'),
        product_url=products[0].get('Product URL')
    )
    product_list.append(final_di)
    return product_list


async def get_chit_chat(query: str):
    entity_mapping = dict()
    # identify the intent of the query
    intent = classify_intent(query)
    if intent == IntentEnum.CHITCHAT.value:
        message_response = generate_chit_chat_response(query)
        entity_mapping['chit_chat'] = {'message': message_response}
        return entity_mapping
    else:
        entities = extract_entities(query)  # entities dict TODO -> handle this through LLM which is being used
        for key, value in entities.items():
            if key and value:
                category = await get_selected_category_items(value)
                entity_mapping['category'] = category
                break
            else:
                products = handle_user_query(query)
                entity_mapping['sub_category'] = products
        return entity_mapping


# ===========================================================================================

async def insert_chatbot_details(schema):
    with use_db_session() as db:
        mapping = dict(name=schema.name, description=schema.description)
        model = PartnerChatbotProfile(**mapping)
        db.add(model)
        db.commit()
        db.refresh(model)
        return mapping


async def seed_the_database():
    with use_db_session() as db:
        customers = [
            Customer(customer_name="prakash"),
            Customer(customer_name="sakshi"),
            Customer(customer_name="sunil"),
            Customer(customer_name="Deepak"),
            Customer(customer_name="Pandey"),
        ]

        # Populate stores
        stores = [
            Store(store_name="Decathlon"),
            Store(store_name="Adidas"),
            Store(store_name="Reebok"),
            Store(store_name="Puma"),
        ]

        # Populate products
        products = [
            Product(product_name="Running shoes"),
            Product(product_name="Badminton"),
            Product(product_name="Hiking shoes"),
            Product(product_name="Football"),
        ]

        # Add customers, stores, and products to the session
        db.add_all(customers)
        db.add_all(stores)
        db.add_all(products)
        db.commit()

        # Populate sales_transactions
        sample_data = [
            SalesTransaction(product_id=1, customer_id=1, store_id=1, sale_amount=200.50,
                             transaction_date=datetime(2023, 1, 5)),
            SalesTransaction(product_id=2, customer_id=2, store_id=1, sale_amount=150.75,
                             transaction_date=datetime(2023, 1, 5)),
            SalesTransaction(product_id=3, customer_id=3, store_id=2, sale_amount=300.10,
                             transaction_date=datetime(2023, 2, 10)),
            SalesTransaction(product_id=3, customer_id=4, store_id=1, sale_amount=250.00,
                             transaction_date=datetime(2023, 2, 15)),
            SalesTransaction(product_id=4, customer_id=5, store_id=2, sale_amount=180.20,
                             transaction_date=datetime(2023, 3, 5)),
            SalesTransaction(product_id=1, customer_id=1, store_id=1, sale_amount=220.50,
                             transaction_date=datetime(2023, 3, 20)),
        ]

        db.bulk_save_objects(sample_data)
        db.commit()

        for _ in range(20):
            partner = Partner(
                uuid=uuid.uuid4(),
                email=faker.email(),
                phone=faker.phone_number(),
                username=faker.user_name(),
                display_name=faker.name(),
                salary=faker.random_int(min=1000, max=9999),
                date_of_birth=faker.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=90),
                email_verified_at=random_date(datetime(2020, 1, 1), datetime(2023, 1, 1)) if random.choice(
                    [True, False]) else None,
                created_at=random_date(datetime(2020, 1, 1), datetime(2023, 1, 1)) if random.choice(
                    [True, False]) else None,
                completed_signup_at=random_date(datetime(2020, 1, 1), datetime(2023, 1, 1)) if random.choice(
                    [True, False]) else None,
            )
            db.add(partner)
            db.commit()
            db.refresh(partner)
        for _ in range(np.random.randint(1, 4)):
            chatbot_profile = PartnerChatbotProfile(
                name=faker.company(),
                description=faker.catch_phrase(),
                partner_id=partner.uuid,
            )
            db.add(chatbot_profile)
            db.commit()
            db.refresh(chatbot_profile)
        return True


def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )
