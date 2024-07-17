import spacy
import random
from spacy.training.example import Example
from spacy.tokens import DocBin

# Load the training data and fine-tune the model
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")
ner.add_label("Liquid Soap Dispensers")
ner.add_label("Laundry Detergent")
ner.add_label("Skin Care")
ner.add_label('Hair Care')
ner.add_label('Gift Card')

# Prepare training data
train_data = [
    ('liquid soap.', {'entities': [(0, 11, 'Liquid Soap')]}),
    ('show me some good liquid soap', {'entities': [(18, 29, 'Liquid Soap')]}),
    ('i want to order liquid soap', {'entities': [(16, 27, 'Liquid Soap')]}),
    ('soap liquid', {'entities': []}),
    ('some liquid soaps', {'entities': [(5, 16, 'Liquid Soap')]}),
    ('pls show me liquid soaps', {'entities': [(12, 23, 'Liquid Soap')]}),
    # -------------------- Laundry Detergent ---------
    ('laundry detergent', {'entities': [(0, 17, 'Laundry Detergent')]}),
    ('show me laundry detergent', {'entities': [(8, 25, 'Laundry Detergent')]}),
    ('I want to order laundry detergent', {'entities': [(16, 33, 'Laundry Detergent')]}),
    ('give me some options of laundry detergent', {'entities': [(24, 41, 'Laundry Detergent')]}),
    ('show me options of laundry detergent', {'entities': [(19, 36, 'Laundry Detergent')]}),
    ('detergent', {'entities': [(0, 9, 'Laundry Detergent')]}),
    ('show me detergent options', {'entities': [(8, 17, 'Laundry Detergent')]}),
    ('I want to order detergent', {'entities': [(16, 25, 'Laundry Detergent')]}),
    ('give me some options of detergent', {'entities': [(24, 33, 'Laundry Detergent')]}),
    ('detergents', {'entities': [(0, 10, 'Laundry Detergent')]}),
    ('detergents options', {'entities': [(0, 10, 'Laundry Detergent')]}),
    # ------------------- Skin Care ------------------------
    ('skin care', {'entities': [(0, 9, 'Skin Care')]}),
    ('i want to order skin care', {'entities': [(16, 25, 'Skin Care')]}),
    ('do you have skin care items?', {'entities': [(12, 21, 'Skin Care')]}),
    ('do you also have skin care items available?', {'entities': [(17, 26, 'Skin Care')]}),
    ('can you show me few skin care products?', {'entities': [(20, 29, 'Skin Care')]}),
    ('products related to skin care', {'entities': [(20, 29, 'Skin Care')]}),
    ('show me few skin care products', {'entities': [(12, 21, 'Skin Care')]}),
    ('fetch me skin care products', {'entities': [(9, 18, 'Skin Care')]}),
    ('skin products', {'entities': [(0, 4, 'Skin Care')]}),
    ('i want to order skin products', {'entities': [(16, 20, 'Skin Care')]}),
    ('do you have skin products?', {'entities': [(12, 16, 'Skin Care')]}),
    ('do you also have skin products available?', {'entities': [(17, 21, 'Skin Care')]}),
    ('can you show me few skin related products?', {'entities': [(20, 24, 'Skin Care')]}),
    ('products related to skin', {'entities': [(20, 24, 'Skin Care')]}),
    ('show me few skin products', {'entities': [(12, 16, 'Skin Care')]}),
    ('fetch me skin products', {'entities': [(9, 13, 'Skin Care')]}),
    ('skin', {'entities': [(0, 4, 'Skin Care')]}),
    # ----------------------------   Hair Care ----------------------------
    ('hair care', {'entities': [(0, 9, 'Hair Care')]}),
    ('i want to order hair care products', {'entities': [(16, 25, 'Hair Care')]}),
    ('do you have hair care items?', {'entities': [(12, 21, 'Hair Care')]}),
    ('do you also have hair care items available?', {'entities': [(17, 26, 'Hair Care')]}),
    ('can you show me few hair care products?', {'entities': [(20, 29, 'Hair Care')]}),
    ('products related to hair care', {'entities': [(20, 29, 'Hair Care')]}),
    ('show me few hair care products', {'entities': [(12, 21, 'Hair Care')]}),
    ('fetch me hair care products', {'entities': [(9, 18, 'Hair Care')]}),
    ('hair products', {'entities': [(0, 4, 'Hair Care')]}),
    ('i want to order hair products', {'entities': [(16, 20, 'Hair Care')]}),
    ('do you have hair products?', {'entities': [(12, 16, 'Hair Care')]}),
    ('do you also have hair products available?', {'entities': [(17, 21, 'Hair Care')]}),
    ('can you show me few hair related products?', {'entities': [(20, 24, 'Hair Care')]}),
    ('products related to hair', {'entities': [(20, 24, 'Hair Care')]}),
    ('show me few hair products', {'entities': [(12, 16, 'Hair Care')]}),
    ('fetch me hair products', {'entities': [(9, 13, 'Hair Care')]}),
    # --------------------- Gift Card --------------------------------
    ('gift card', {'entities': [(0, 9, 'Gift Card')]}),
    ('do you also have git card?', {'entities': []}),
    ('show me gift card', {'entities': [(8, 17, 'Gift Card')]}),
    ('gift cards', {'entities': [(0, 10, 'Gift Card')]}),
    ('do you also have git cards?', {'entities': []}),
    ('show me gift cards', {'entities': [(8, 18, 'Gift Card')]})
]

# Convert the training data to SpaCy's format
db = DocBin()
for text, annot in train_data:
    doc = nlp.make_doc(text)
    ents = [doc.char_span(start, end, label=label) for start, end, label in annot["entities"]]
    ents = [e for e in ents if e is not None]  # Filter out None values
    doc.ents = ents
    db.add(doc)
db.to_disk("./train.spacy")

# Fine-tune the model

# Load the saved DocBin from disk
db = DocBin().from_disk("./train.spacy")

optimizer = nlp.begin_training()

for i in range(20):
    random.shuffle(train_data)  # instead this use db -> random.shuffle(db)
    losses = {}
    for text, annotations in train_data:
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], drop=0.35, losses=losses)
    print(losses)

# Save the fine-tuned model
nlp.to_disk("../NER_MODELS/custom_ner_model")
