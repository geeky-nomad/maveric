import pandas as pd
import spacy

# Load custom NER model
MODEL_TO_LOAD = "mav_structure/NER_MODELS/custom_ner_model"
# MODEL_TO_LOAD = "../NER_MODELS/custom_ner_model"  # when not running via Docker

nlp = spacy.load(MODEL_TO_LOAD)


def extract_entities(text):
    doc = nlp(text)
    entities = {"liquid_soap": "", "laundry_detergent": "", "skin_care": "", 'hair_care': "", "gift_card": ""}
    for ent in doc.ents:
        if ent.label_ == "Liquid Soap Dispensers":
            entities['liquid_soap'] = ent.label_
        elif ent.label_ == "Laundry Detergent":
            entities['laundry_detergent'] = ent.label_
        elif ent.label_ == "Skin Care":
            entities['skin_care'] = ent.label_
        elif ent.label_ == 'Hair Care':
            entities['hair_care'] = ent.label_
        elif ent.label_ == 'Gift Card':
            entities['gift_card'] = ent.label_
    print('Extracted entities are -------->', entities)
    return entities
