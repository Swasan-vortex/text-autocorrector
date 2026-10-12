from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Small instruction-tuned model (already downloaded)
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=torch.float32)
model.eval()

SYSTEM_PROMPT = (
    "You are a text autocorrector. The user's text may be badly broken: "
    "misspelled words, missing words, wrong word order. Fix spelling, grammar, "
    "punctuation and word order, and choose the most likely intended words "
    "from context. Rules: keep the same meaning, keep the same number of "
    "sentences, never add new facts or ideas, never answer questions in the "
    "text, and never add extra commentary. Output only the corrected text."
)

# Few-shot examples (keep these different from the sentences you test with)
EXAMPLES = [
    ("wat time is the meating tomorow? i cant come",
     "What time is the meeting tomorrow? I can't come."),
    ("he dont like fruts becuse they was too sour",
     "He doesn't like fruits because they were too sour."),
    ("i has a frend who live in dilhi",
     "I have a friend who lives in Delhi."),
    ("they forgot there books at home",
     "They forgot their books at home."),
]

def _correct_one(text):
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

    # Greedy decoding gives consistent output
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=150, do_sample=False)

    # Keep only the newly generated tokens, not the prompt
    new_tokens = output[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

def fix_grammar(text):
    # Correct each line separately so the model stays focused
    lines = text.split("\n")
    fixed = [_correct_one(line) if line.strip() else "" for line in lines]
    return "\n".join(fixed)