import re
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

csv_path = 'mav_structure/Data/hiketron.csv'
df = None
model = None
embeddings = None
index = None


def load_rag():
    global df, model, embeddings, index
    # Load the dataset
    df = pd.read_csv(csv_path)
    df['combined_features'] = df['Title'] + ' ' + df['Variant Price'].astype(str) + ' ' + df['Type']

    # Load the SentenceTransformer model and create embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df['combined_features'].tolist())

    # Create a FAISS index and add the embeddings
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Create a FAISS index and add the embeddings
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)


def parse_price_constraints(query):
    price_constraints = {}
    less_than = re.search(r'less than (\d+)', query)
    more_than = re.search(r'more than (\d+)', query)
    between = re.search(r'between (\d+) and (\d+)', query)

    if less_than:
        price_constraints['less_than'] = int(less_than.group(1))
    if more_than:
        price_constraints['more_than'] = int(more_than.group(1))
    if between:
        price_constraints['between'] = (int(between.group(1)), int(between.group(2)))

    return price_constraints


def filter_by_price(df, constraints):
    if 'less_than' in constraints:
        df = df[df['Variant Price'] < constraints['less_than']]
    if 'more_than' in constraints:
        df = df[df['Variant Price'] > constraints['more_than']]
    if 'between' in constraints:
        df = df[(df['Variant Price'] >= constraints['between'][0]) & (df['Variant Price'] <= constraints['between'][1])]

    return df


def handle_user_query(user_query, top_k=2):
    constraints = parse_price_constraints(user_query)
    filtered_df = filter_by_price(df, constraints)

    if not filtered_df.empty:
        filtered_embeddings = model.encode(filtered_df['combined_features'].tolist())
        filtered_index = faiss.IndexFlatL2(filtered_embeddings.shape[1])
        filtered_index.add(filtered_embeddings)

        query_embedding = model.encode([user_query])
        D, I = filtered_index.search(query_embedding, top_k)
        results = filtered_df.iloc[I[0]]
    else:
        query_embedding = model.encode([user_query])
        D, I = index.search(query_embedding, top_k)
        results = df.iloc[I[0]]

    # Convert matched records to JSON-serializable format
    final_list = results[['Handle']].to_dict(orient='records')
    response_list = [
        {
            'text': ' '.join(word.capitalize() for word in _handle.get('Handle').split('-')),
            'value': _handle.get('Handle')
        }
        for _handle in final_list
    ]

    return response_list
