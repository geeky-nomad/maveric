import gradio as gr
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the CSV file into a DataFrame
df = pd.read_csv('FashionDataset_New.csv')

# Predefined responses
greetings = ["hi", "hello", "hey", "greetings"]
farewells = ["bye", "goodbye", "see you", "take care"]


def preprocess_query(query):
    return query.lower().split()


def compute_cosine_similarity(df, column_name, query):
    vectorizer = CountVectorizer().fit([query] + df[column_name].astype(str).tolist())
    query_vector = vectorizer.transform([query])
    column_vectors = vectorizer.transform(df[column_name].astype(str))
    cos_similarities = cosine_similarity(query_vector, column_vectors)[0]
    df['cos_similarity'] = cos_similarities
    return df.nlargest(10, 'cos_similarity')


def find_best_matches(user_query):
    query_tokens = preprocess_query(user_query)

    # Check for the highest match in BrandName column
    brand_matches = compute_cosine_similarity(df, 'BrandName', user_query)

    if brand_matches.iloc[0]['cos_similarity'] > 0:
        highest_priority_df = brand_matches
        colour_matches = compute_cosine_similarity(highest_priority_df, 'Colour', user_query)
        if colour_matches.iloc[0]['cos_similarity'] > 0:
            highest_priority_df = colour_matches
    else:
        # Check for the highest match in Colour column if no significant BrandName match
        colour_matches = compute_cosine_similarity(df, 'Colour', user_query)

        if colour_matches.iloc[0]['cos_similarity'] > 0:
            highest_priority_df = colour_matches
        else:
            # Fallback to matching with Details column
            highest_priority_df = df

    # Now filter the DataFrame based on the highest priority match found above
    filtered_df = highest_priority_df

    # Compute cosine similarity with the Details column for filtered records
    vectorizer = CountVectorizer().fit([user_query] + filtered_df['Details'].astype(str).tolist())
    query_vector = vectorizer.transform([user_query])
    details_vectors = vectorizer.transform(filtered_df['Details'].astype(str))
    cos_similarities = cosine_similarity(query_vector, details_vectors)[0]

    # Add cosine similarities to DataFrame
    filtered_df = filtered_df.copy()
    filtered_df['cos_similarity'] = cos_similarities

    # Get top 3 results based on cosine similarity
    top_results = filtered_df.nlargest(2, 'cos_similarity')

    return top_results[['BrandName', 'Colour', 'Details', 'cos_similarity']]


def chatbot_response(user_input, conversation_history):
    user_input = user_input.lower()
    conversation_history.append(["You:", user_input])  # Append user input to conversation history

    if any(greeting in user_input for greeting in greetings):
        bot_response = "Hello! How can I assist you with your product search today?"
        conversation_history.append(["Bot:", bot_response])  # Append bot response to conversation history

    elif any(farewell in user_input for farewell in farewells):
        bot_response = "Goodbye! Have a great day!"
        conversation_history.append(["Bot:", bot_response])  # Append bot response to conversation history
        return conversation_history, conversation_history

    else:
        # Get the best matches based on user query
        matches = find_best_matches(user_input)
        response = "Here are the top 3 products that match your query:\n"
        for index, row in matches.iterrows():
            response += f"Brand: {row['BrandName']}, Colour: {row['Colour']}, Details: {row['Details']}\n"
        bot_response = response
        conversation_history.append(["Bot:", bot_response])  # Append bot response to conversation history

    return conversation_history, conversation_history  # Return updated conversation history


# Initialize Gradio interface
iface = gr.Interface(
    fn=chatbot_response,
    inputs=[
        gr.Textbox(label="You: ", placeholder="Type your message here..."),
        gr.State([])  # Initial conversation history is an empty list
    ],
    outputs=[
        gr.Chatbot(label="Chat History"),  # Using Chatbot component to display conversation
        gr.State()  # State to hold conversation history
    ],
    live=False
)

iface.launch()
