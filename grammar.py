from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Pre-trained grammar correction model (pehli baar chalne par download hoga)
MODEL_NAME = "vennify/t5-base-grammar-correction"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def fix_grammar(text):
    inputs = tokenizer("grammar: " + text, return_tensors="pt",
                       truncation=True, max_length=256)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=128, num_beams=4)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    sample = "I has went to there house yesterday and they was not at home."
    print("Before:", sample)
    print("After: ", fix_grammar(sample))