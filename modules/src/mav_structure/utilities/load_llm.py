# Load the fine-tuned model and tokenizer
from transformers import AutoModelForCausalLM, AutoTokenizer

model = None
tokenizer = None


def load_model():
    global model, tokenizer
    llm_file_to_load = 'mav_structure/LLM_MODELS/fine-tuned-dialoGPT'
    model = AutoModelForCausalLM.from_pretrained(llm_file_to_load)
    tokenizer = AutoTokenizer.from_pretrained(llm_file_to_load)


def generate_chit_chat_response(query):
    # Encoding the input
    input_ids = tokenizer.encode(query + tokenizer.eos_token, return_tensors='pt')
    # Generate the response
    response_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    # Decode the generated response
    response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response
