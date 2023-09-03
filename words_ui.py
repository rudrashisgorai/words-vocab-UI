import streamlit as st
import json
import pickle
import pandas as pd

st.set_page_config(layout="wide")


# Function to load dictionary from pickle file
def load_dictionary_from_pkl(filepath):
    with open(filepath, "rb") as f:
        return pickle.load(f)


# Initialize list to keep track of last searched words
if "key" not in st.session_state:
    st.session_state["key"] = []


# Path to the pickle file
pickle_file_path = "words_dicts_extended (1).pkl"

# Load the dictionary
try:
    my_dict = load_dictionary_from_pkl(pickle_file_path)
except FileNotFoundError:
    my_dict = {}
    st.write(f"File {pickle_file_path} not found.")

# Streamlit App
st.title("Word Search in Dictionary")

# Side Panel
st.sidebar.title("Features")
sidebar_input = st.sidebar.text_input("Search a new word on Vocabulary.com:")

# User input
search_word = st.selectbox("Select a word to search:", (i for i in my_dict.keys()))

# Sidebar search functionality for Vocabulary.com
if sidebar_input:
    url = f"https://www.vocabulary.com/dictionary/{sidebar_input}"
    st.sidebar.markdown(
        f"[Click here to look up '{sidebar_input}' on Vocabulary.com]({url})"
    )

st.sidebar.write(set(st.session_state.key))
# Search in dictionary and update last_searched_words
if search_word:
    value = my_dict.get(search_word, "Not Found")
    st.session_state.key.append(search_word)

    if value != "Not Found":
        st.subheader(
            f" Details for word: {search_word}",
        )
        # print(value)
        try:
            df = pd.DataFrame(value["results"])

            # Display the word and its properties
            st.text(f"Pronunciation: {value['pronunciation']['all']}")
            st.text(f"Syllables: {', '.join(value['syllables']['list'])}")
            st.text(f"Frequency: {value['frequency']}")

            st.table(df)
        except:
            st.json(value)

    else:
        word = search_word  # Replace with the word you want to look up
        url = f"https://www.vocabulary.com/dictionary/{word}"
        st.write(f"Word '{search_word}' not found in the dictionary.")
        st.markdown(f"[Click here to look up '{word}' on Vocabulary.com]({url})")


st.sidebar.write("### List of Available Words:")
st.sidebar.write((my_dict.keys()))  # List all the predefined words
