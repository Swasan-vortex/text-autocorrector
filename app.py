from corrector import correct_text
from grammar import fix_grammar

def full_correct(text):
    step1 = correct_text(text)   # pehle spelling theek karo
    step2 = fix_grammar(step1)   # phir grammar aur context
    return step1, step2

if __name__ == "__main__":
    sample = "I realy like lerning about artifical inteligence, she dont know there answer."
    spelled, final = full_correct(sample)
    print("Original :", sample)
    print("Spelling :", spelled)
    print("Final    :", final)