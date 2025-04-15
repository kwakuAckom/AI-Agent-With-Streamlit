import os, time
import langchain_core
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st


load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

st.title("LangChain Groq Chatbot")
st.write("This is a simple chatbot using LangChain and Groq.")
chat = ChatGroq(
    temperature = 0,
    groq_api_key = API_KEY,
    model_name = "llama-3.1-8b-instant",
    streaming= True)

actor = st.text_area("Define the behavior of this AI agent (i.e. 'You are a professional coding assistant that provides explanation and code in an appropriate programming language about a topic')",
                     placeholder="You are a professional coding assistant ...",)

prog = st.selectbox("Select a programming language:", ["Python", "Java", "JavaScript", "C++"])


if actor:
    actor
else:
    actor = 'You are a professional coding assistant that provides explanation and code in an appropriate programming language about a topic'
prompt = ChatPromptTemplate.from_messages([
            "system", actor + "{topic}.",
            "human","What can you tell me about {topic}?",
            "assistant","Here is some information about {topic}."])

output_parser = StrOutputParser()

chain = prompt | chat | output_parser



user_input = st.text_input("Enter a topic:")
# user_input = st.chat_input("Type your message here...")

user_input = user_input + " in " + prog
response = chain.invoke({"topic": user_input})
state = st.button("Generate")

def stream_response(response):
    """Simulate streaming response by iterating over the response string."""
    if state and user_input:
        st.write("### Sure, here is the information about:", user_input)  # Add a section header for clarity
        
        # Create a placeholder for streaming the response
        response_placeholder = st.empty()
        
        # Initialize an empty string to accumulate the response
        accumulated_response = ""
        
        # Simulate streaming by iterating over the response (assuming response is iterable)
        for word in response.split():
            accumulated_response += word + " "  # Add the current word to the accumulated response
            response_placeholder.markdown(f"**{accumulated_response.strip()}**")  # Update the placeholder with formatted text
            time.sleep(0.1)  # Add a small delay to simulate streaming
if state and user_input:
    with st.spinner("Generating..."):
        st.write("Sure, here is the information about", user_input)
        st.write(response)

