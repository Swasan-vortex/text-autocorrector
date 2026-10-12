import streamlit as st
from grammar import fix_grammar

st.set_page_config(page_title="Text Autocorrector", page_icon="✍️")

st.title("✍️ Text Autocorrector for Error-Free Writing")
st.write("Type or paste your text. The app fixes spelling and grammar together.")

text = st.text_area(
    "Your text",
    height=150,
    placeholder="e.g. I realy like lerning, she dont know there answer.",
)

if st.button("Correct my text"):
    if text.strip():
        with st.spinner("Correcting..."):
            final = fix_grammar(text)
        st.subheader("Before")
        st.write(text.replace("\n", "  \n"))
        st.subheader("Final corrected text")
        st.success(final.replace("\n", "  \n"))
    else:
        st.warning("Please enter some text first.")