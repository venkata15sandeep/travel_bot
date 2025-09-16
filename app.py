import streamlit as st
from dotenv import load_dotenv
import os

@st.cache_resource
def interact_With_llm():
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.output_parsers import StrOutputParser
    from langchain_community.chat_message_histories import ChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory

    # --- prompt ---
    prompt = ChatPromptTemplate.from_messages([
        ("system", "you are a helpful assistant that helps people with their travel plan queries."),
        ("human", "I want to visit {place} for {no_of_days} days. Can you suggest an itinerary?"),
        ("human", "I am interested in {any_specific_interest}."),
    ])
    load_dotenv()  # take environment variables from .env.
    # --- LLM---
    llm = ChatGoogleGenerativeAI(
        model = "gemini-1.5-flash",
        google_api_key = os.getenv("GOOGLE_API_KEY"),
        temperature=0.2 
    )

    chain = prompt | llm
    return chain

st.session_state.setdefault("response", "" ) # to store the response

st.title("Travel Bot")

st.write("Ask me anything about your travel plans!")

st.text_area(label="Response", value=st.session_state.get("response"), height=200)

place = st.text_input("Your place of visit:")

no_of_days = st.number_input("Number of days:", min_value=1, max_value=30)

any_specific_interest = st.text_input("Any specific interests (e.g., adventure, relaxation, culture)?")

if st.button("Get Answer"):
    if place:
        chain = interact_With_llm()
        response = chain.invoke({"place": place, "no_of_days": no_of_days, "any_specific_interest": any_specific_interest}).content    
        st.session_state.response = response
        st.rerun()
    else:
        st.warning("Please enter a place.")