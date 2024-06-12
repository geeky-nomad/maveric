import spacy
from spacy.tokens import DocBin

# Load the training data and fine-tune the model
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")
ner.add_label("COLOR")
ner.add_label("BRAND")
ner.add_label("CATEGORY")
ner.add_label('NEGATION')


# Prepare training data
train_data = [
    ("Show me a red Zara top.", {"entities": [(10, 13, "COLOR"), (14, 18, "BRAND"), (19, 22, "CATEGORY")]}),
    ("Show me a blue Zara dress.", {"entities": [(10, 14, "COLOR"), (15, 19, "BRAND"), (20, 25, "CATEGORY")]}),
    ("a grey t-shirt.", {"entities": [(2, 6, "COLOR"), (7, 14, "CATEGORY")]}),
    ("grey t-shirt.", {"entities": [(0, 4, "COLOR"), (5, 12, "CATEGORY")]}),
    ("red t-shirt.", {"entities": [(0, 3, "COLOR"), (4, 11, "CATEGORY")]}),
    ("off white shirt.", {"entities": [(0, 9, "COLOR"), (10, 15, "CATEGORY")]}),
    ("off white t-shirt.", {"entities": [(0, 9, "COLOR"), (10, 17, "CATEGORY")]}),
    ("dark blue t-shirt.", {"entities": [(0, 9, "COLOR"), (10, 17, "CATEGORY")]}),
    ("regular top.", {"entities": [(0, 11, "CATEGORY")]}),
    ("regular dress.", {"entities": [(0, 13, "CATEGORY")]}),
    ("shirt.", {"entities": [(0, 5, "CATEGORY")]}),
    ("jeans.", {"entities": [(0, 5, "CATEGORY")]}),
    ("t-shirt.", {"entities": [(0, 7, "CATEGORY")]}),
    ("trousers.", {"entities": [(0, 8, "CATEGORY")]}),
    ("loungewear short set.", {"entities": [(0, 20, "CATEGORY")]}),
    ("track pants.", {"entities": [(0, 11, "CATEGORY")]}),
    ("casual shirt.", {"entities": [(0, 12, "CATEGORY")]}),
    ("tights.", {"entities": [(0, 6, "CATEGORY")]}),
    # -------------------- Brand variations ---------
    ("vero moda.", {"entities": [(0, 9, "BRAND")]}),
    ("vera moda.", {"entities": [(0, 9, "BRAND")]}),
    ("vera moda shirts.", {"entities": [(0, 9, "BRAND"), (10, 16, "CATEGORY")]}),
    ("vero moda t-shirts.", {"entities": [(0, 9, "BRAND"), (10, 18, "CATEGORY")]}),
    ("van heusen.", {"entities": [(0, 10, "BRAND")]}),
    ("madame.", {"entities": [(0, 6, "BRAND")]}),
    ("allen solly.", {"entities": [(0, 11, "BRAND")]}),
    ("life.", {"entities": [(0, 4, "BRAND")]}),
    ("only.", {"entities": [(0, 4, "BRAND")]}),
    ("adidas.", {"entities": [(0, 6, "BRAND")]}),
    ("pepe.", {"entities": [(0, 4, "BRAND")]}),
    ("kashish.", {"entities": [(0, 7, "BRAND")]}),
    ("ed hardy.", {"entities": [(0, 8, "BRAND")]}),
    ("stop.", {"entities": [(0, 4, "BRAND")]}),
    ("rare.", {"entities": [(0, 4, "BRAND")]}),
    ("pepe.", {"entities": [(0, 4, "BRAND")]}),
    # ----------- Colour variations--------------
    ("yellow.", {"entities": [(0, 6, "COLOR")]}),
    ("orange.", {"entities": [(0, 6, "COLOR")]}),
    ("olive.", {"entities": [(0, 5, "COLOR")]}),
    ("brown.", {"entities": [(0, 5, "COLOR")]}),
    ("dark brown.", {"entities": [(0, 10, "COLOR")]}),
    ("pink", {"entities": [(0, 4, "COLOR")]}),
    ("baby pink.", {"entities": [(0, 9, "COLOR")]}),
    ("sage.", {"entities": [(0, 4, "COLOR")]}),
    # Negation examples
    ("I want a t-shirt but don't want a pink color.", {"entities": [(9, 16, "CATEGORY"), (21, 26, "NEGATION"), (34, 38, "COLOR")]}),
    ("I don't want a red dress.", {"entities": [(2, 7, "NEGATION"), (15, 18, "COLOR"), (20, 25, "CATEGORY")]}),
    ("show me other than pink.", {"entities": [(8, 18, "NEGATION"), (19, 23, "COLOR")]}),
    ("not in pink.", {"entities": [(0, 3, "NEGATION"), (7, 11, "COLOR")]}),
    ("not in red.", {"entities": [(0, 3, "NEGATION"), (7, 10, "COLOR")]}),
    ("not white.", {"entities": [(0, 3, "NEGATION"), (4, 9, "COLOR")]})
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
import random
from spacy.training.example import Example

optimizer = nlp.begin_training()
for i in range(20):
    random.shuffle(train_data)
    losses = {}
    for text, annotations in train_data:
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], drop=0.35, losses=losses)
    print(losses)

# Save the fine-tuned model
nlp.to_disk("custom_ner_model")
