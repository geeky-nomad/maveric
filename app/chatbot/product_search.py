# import pandas as pd
# import spacy
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import nltk
#
# stopwords = nltk.corpus.stopwords.words('english')
# # update stopwords as per the requirements
# stopwords.remove('only')
#
# # Set pandas display options to show full column content
# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_columns', None)
#
# # Load the e_commerce.csv file
# df = pd.read_csv('nlp_fashion.csv')
#
# # Load custom NER model
# nlp = spacy.load("custom_ner_model")
#
#
# def extract_entities(text):
#     text = ' '.join(text)
#     doc = nlp(text)
#     entities = {"brand": "", "color": "", "category": "", 'negation': ""}
#     for ent in doc.ents:
#         if ent.label_ == "BRAND":
#             entities['brand'] = ent.text
#         elif ent.label_ == "COLOR":
#             entities['color'] = ent.text
#         elif ent.label_ == "CATEGORY":
#             entities['category'] = ent.text
#         elif ent.label_ == 'NEGATION':
#             entities['negation'] = ent.text
#
#     # Handle negation
#     if entities.get("negation"):
#         # remove colour for now, later _> negation can be applied to category or in Brand also
#         # we have to find z way to implement this
#         del entities['color']
#     return entities
#
#
# def create_query_text(entities):
#     # Join non-empty values with a space
#     query_parts = [value for value in entities.values() if value]
#     return ' '.join(query_parts)
#
#
# def match_score(row, entities):
#     score = 0
#     if entities.get('brand') and entities['brand'].lower() in str(row['BrandName']).lower():
#         score += 1
#     if entities.get('color') and entities['color'].lower() in str(row['Colour']).lower():
#         score += 1
#     if entities.get('category') and entities['category'].lower() in str(row['Category']).lower():
#         score += 1
#     return score
#
#
# def search_entities_in_df(user_query):
#     # Extract entities from user query
#     entities = extract_entities(user_query)
#     # Compute the exact match score for each row
#     df['match_score'] = df.apply(lambda row: match_score(row, entities), axis=1)
#
#     # Prioritize rows with the highest match scores
#     exact_matches = df[df['match_score'] > 0].sort_values(by='match_score', ascending=False)
#
#     # If exact matches are found, return them (up to top 3)
#     if not exact_matches.empty:
#         return exact_matches.head(3)
#
#     # If no exact matches, perform similarity search
#     # Combine the relevant columns into a single string for each row
#     df['combined'] = df.apply(lambda row: ' '.join([
#         str(row['BrandName']),
#         str(row['Details']),
#         str(row['Category']),
#         str(row['Colour']),
#     ]), axis=1)
#
#     # Create a search string from the entities
#     search_string = ' '.join(entities.values())
#
#     # Vectorize the text data
#     vectorizer = CountVectorizer().fit_transform([search_string] + df['combined'].tolist())
#     vectors = vectorizer.toarray()
#
#     # Compute cosine similarity between the search string and all rows in the DataFrame
#     cosine_sim = cosine_similarity(vectors)
#     similarity_scores = cosine_sim[0][1:]  # Exclude the first element which is the search string itself
#
#     # Add similarity scores to the DataFrame and sort by these scores
#     df['similarity'] = similarity_scores
#     top_results = df.sort_values(by='similarity', ascending=False).head(3)
#     return top_results[['BrandName', 'Colour', 'Category', 'SellPrice', 'combined', 'similarity']]
#
#
# greetings = ["hello", "hi", "hey", "greetings"]
# farewells = ["bye", "goodbye", "see you", "farewell"]
#
#
# # Define the chatbot response function
# def chatbot_response(user_input, conversation_history):
#     user_input = user_input.lower()
#     user_input = user_input.split()
#
#     if any(greeting in user_input for greeting in greetings):
#         bot_response = "Hello! How can I assist you with your product search today?"
#         conversation_history.append(f"Bot: {bot_response}")  # Append bot response to conversation history
#         return conversation_history, False
#
#     elif any(farewell in user_input for farewell in farewells):
#         bot_response = "Goodbye! Have a great day!"
#         conversation_history.append(f"Bot: {bot_response}")  # Append bot response to conversation history
#         return conversation_history, True  # Indicate the end of conversation
#
#     else:
#         # Get the best matches based on user query
#         matches = search_entities_in_df(user_input)
#         response = "Here are the top 3 products that match your query:\n"
#         for index, row in matches.iterrows():
#             response += f"Brand: {row['BrandName']}, Colour: {row['Colour']}, Category: {row['Category']}\n"
#         bot_response = response
#         conversation_history.append(f"Bot: {bot_response}")  # Append bot response to conversation history
#
#     return conversation_history, False  # Continue conversation
#
#
# def main():
#     conversation_history = []
#     end_chat = False
#
#     print("Welcome to the product search chatbot! Type 'bye' to end the conversation.")
#
#     while not end_chat:
#         user_input = input("You: ")
#         conversation_history, end_chat = chatbot_response(user_input, conversation_history)
#         for message in conversation_history:  # Display the last exchange
#             print(message)
#         conversation_history.clear()
#
#
# if __name__ == "__main__":
#     main()


import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# Download stopwords if not already downloaded
nltk.download('stopwords')

# Load stopwords and remove 'only' as per requirements
stopwords = set(nltk.corpus.stopwords.words('english'))
stopwords.discard('only')

# Set pandas display options to show full column content
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

# Load the e_commerce.csv file
df = pd.read_csv('nlp_fashion.csv')

# Load custom NER model
nlp = spacy.load("custom_ner_model")


def extract_entities(text):
    text = ' '.join(text)
    doc = nlp(text)
    entities = {"brand": "", "color": "", "category": "", 'negation': ""}
    for ent in doc.ents:
        if ent.label_ == "BRAND":
            entities['brand'] = ent.text
        elif ent.label_ == "COLOR":
            entities['color'] = ent.text
        elif ent.label_ == "CATEGORY":
            entities['category'] = ent.text
        elif ent.label_ == 'NEGATION':
            entities['negation'] = ent.text

    # Handle negation
    if entities.get("negation"):
        entities['color'] = ""
    return entities


def create_query_text(entities):
    return ' '.join(value for value in entities.values() if value)


def match_score(row, entities):
    score = 0
    if entities.get('brand') and entities['brand'].lower() in str(row['BrandName']).lower():
        score += 1
    if entities.get('color') and entities['color'].lower() in str(row['Colour']).lower():
        score += 1
    if entities.get('category') and entities['category'].lower() in str(row['Category']).lower():
        score += 1
    return score


def search_entities_in_df(user_query):
    entities = extract_entities(user_query)
    df['match_score'] = df.apply(lambda row: match_score(row, entities), axis=1)

    exact_matches = df[df['match_score'] > 0].sort_values(by='match_score', ascending=False)
    if not exact_matches.empty:
        return exact_matches.head(3)

    df['combined'] = df.apply(lambda row: ' '.join([
        str(row['BrandName']),
        str(row['Details']),
        str(row['Category']),
        str(row['Colour']),
    ]), axis=1)

    search_string = create_query_text(entities)
    vectorizer = CountVectorizer().fit_transform([search_string] + df['combined'].tolist())
    vectors = vectorizer.toarray()

    cosine_sim = cosine_similarity(vectors)
    similarity_scores = cosine_sim[0][1:]

    df['similarity'] = similarity_scores
    top_results = df.sort_values(by='similarity', ascending=False).head(3)
    return top_results[['BrandName', 'Colour', 'Category', 'SellPrice', 'combined', 'similarity']]


greetings = {"hello", "hi", "hey", "greetings"}
farewells = {"bye", "goodbye", "see you", "farewell"}


def chatbot_response(user_input, conversation_history):
    user_input = user_input.lower().split()

    if greetings & set(user_input):
        bot_response = "Hello! How can I assist you with your product search today?"
        conversation_history.append(f"Bot: {bot_response}")
        return conversation_history, False

    elif farewells & set(user_input):
        bot_response = "Goodbye! Have a great day!"
        conversation_history.append(f"Bot: {bot_response}")
        return conversation_history, True

    else:
        matches = search_entities_in_df(user_input)
        if matches.empty:
            bot_response = "Sorry, no matches found."
        else:
            response = "Here are the top 3 products that match your query:\n"
            for index, row in matches.iterrows():
                response += f"Brand: {row['BrandName']}, Colour: {row['Colour']}, Category: {row['Category']}\n"
            bot_response = response
        conversation_history.append(f"Bot: {bot_response}")
        return conversation_history, False


def main():
    conversation_history = []
    end_chat = False

    print("Welcome to the product search chatbot! Type 'bye' to end the conversation.")

    while not end_chat:
        user_input = input("You: ")
        conversation_history, end_chat = chatbot_response(user_input, conversation_history)
        print(conversation_history[-1])
        conversation_history.clear()


if __name__ == "__main__":
    main()

