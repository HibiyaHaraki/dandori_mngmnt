#
# May 2025. Created by Hibiya Haraki
#
# Compare_Text.py
#

from transformers import BertTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine

#Compare text setting
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Convert string to vector
def get_sentence_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

# Compare text
def compare_text(text1, text2,threshold=0.9):
    vec1 = get_sentence_embedding(text1)
    vec2 = get_sentence_embedding(text2)

    similarity = 1 - cosine(vec1, vec2)
    print("Similarity: {}".format(similarity))

    if similarity > threshold:
        return True
    else:
        return False