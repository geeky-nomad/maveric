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
from mav_structure.NLP.product_search import extract_entities

# Faker instance
faker = Faker()

csv_path = 'mav_structure/Data/hiketron.csv'
df = pd.read_csv(csv_path)


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
    category = df[df['Type'] == category]['Handle'].tolist()
    # convert category in the format {'text': '', 'value': ''}
    mapping_categories = [{'text': ' '.join(word.capitalize() for word in _item.split('-')), 'value': _item} for _item
                          in category]
    return mapping_categories


async def get_selected_category_products(sub_category):
    product_list = []
    df_filtered = df[df['Handle'] == sub_category]
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
    intents = {
        'chit_chat': ['Hi', 'Hello', 'Hey'],
        'product_search': []
    }
    if query.capitalize() in intents.get('chit_chat'):
        welcome = await product_categories()
        entity_mapping['chit_chat'] = welcome
        return entity_mapping
    else:
        entities = extract_entities(query)  # entities dict
        for key, value in entities.items():
            if key and value:
                category = await get_selected_category_items(value)
                entity_mapping['category'] = category
                break
            else:
                products = await find_similar_product(query)
                entity_mapping['sub_category'] = products
        return entity_mapping

# Load BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Precompute embeddings for product handles
handle_embeddings = model.encode(df['Handle'].tolist(), convert_to_tensor=True)

async def find_similar_product(query):
    # Embed the user query
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Compute cosine similarity between query and handles
    similarities = util.pytorch_cos_sim(query_embedding, handle_embeddings).flatten()

    # Find the indices of the top 3 most similar handles
    top_indices = similarities.argsort(descending=True)[:2]

    # Retrieve the matched records
    matched_records = df.iloc[top_indices]

    # Convert matched records to JSON-serializable format with only Handle and ImageSrc
    final_list = matched_records[['Handle']].to_dict(orient='records')
    _li = [
        {
            'text': ' '.join(word.capitalize() for word in _handle.get('Handle').split('-')),
            'value': _handle.get('Handle')
        }
        for _handle in final_list
    ]

    return _li

# async def find_similar_product(query):
#     vectorizer = TfidfVectorizer()
#     handle_vectors = vectorizer.fit_transform(df['Handle'])
#     query_vec = vectorizer.transform([query])
#
#     # Compute cosine similarity
#     similarity = cosine_similarity(query_vec, handle_vectors).flatten()
#
#     # Find the index of the most similar handle
#     most_similar_index = similarity.argmax()
#
#     # Retrieve the price and image source
#     matched_record = df.iloc[most_similar_index]
#     record_handle = matched_record.to_dict()
#     final_list = [
#         {
#             'text': ' '.join(word.capitalize() for word in record_handle.get('Handle').split('-')),
#             'value': record_handle.get('Handle')
#         }
#     ]
#     return final_list


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
