from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Small instruction-tuned model (about 3 GB, downloaded on first run)
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=torch.float32)
model.eval()

SYSTEM_PROMPT = (
    "You are a text autocorrector. The user's text may be badly broken: "
    "misspelled words, missing words, wrong word order. Infer the most likely "
    "intended meaning from context and rewrite it as correct, natural English. "
    "Fix spelling, grammar, punctuation and word order. Keep the original "
    "meaning. Output only the corrected text, nothing else."
)

# Few-shot examples that show the model the expected behavior
EXAMPLES = [
    ("how old you? my nme is sam",
     "How old are you? My name is Sam."),
    ("she dont no wer is the libary",
     "She doesn't know where the library is."),
]

def fix_grammar(text):
    # Build the chat: system prompt, then examples, then the user's text
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for bad, good in EXAMPLES:
        messages.append({"role": "user", "content": bad})
        messages.append({"role": "assistant", "content": good})
    messages.append({"role": "user", "content": text})

    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(prompt, return_tensors="pt")

    # Greedy decoding (do_sample=False) gives consistent output
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=150, do_sample=False)

    # Keep only the newly generated tokens, not the prompt
    new_tokens = output[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()