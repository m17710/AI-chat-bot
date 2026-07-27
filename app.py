import os
import groq
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")
MODEL_NAME = "openai/gpt-oss-20b"

st.set_page_config(page_title="AI Q&A Chatbot", page_icon="🤖", layout="centered")

if "history" not in st.session_state:
    st.session_state.history = []

if "chat_error" not in st.session_state:
    st.session_state.chat_error = ""

if "question_input" not in st.session_state:
    st.session_state.question_input = ""

client = None
if API_KEY:
    try:
        client = Groq(api_key=API_KEY)
    except Exception as e:
        st.session_state.chat_error = f"Failed to create Groq client: {e}"

st.title("🤖 AI Q&A Chatbot")
st.write("Ask any question related to AI and data science and receive an AI-generated answer using the Groq API.")

with st.expander("How it works", expanded=False):
    st.write(
        "This app sends your question to Groq, receives an AI response, and displays the answer in the browser. "
        "Your API key is loaded from `.env` and never stored in source control."
    )

question = st.text_area("Your question", key="question_input", height=120, max_chars=800)
char_count = len(question)
st.caption(f"Character count: {char_count}/800")


def ask_callback():
    st.session_state.chat_error = ""
    question = st.session_state.question_input
    if not question.strip():
        st.error("Please type a question before clicking Ask.")
        return
    with st.spinner("Waiting for AI response..."):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful  coding assistant you will help to understand only python concepts and libraries machine learning and data sciece techniques and you will only respond if the question is related to the given context context which i defined ."},
                    {"role": "user", "content": question.strip()},
                ],
                model=MODEL_NAME,
            )
            answer = response.choices[0].message.content.strip()
            if not answer:
                answer = "The model returned an empty response. Please try again."
            st.session_state.history.append({"question": question.strip(), "answer": answer})
        except groq.APIConnectionError:
            st.session_state.chat_error = "Could not reach the Groq API. Check your internet connection."
        except groq.RateLimitError:
            st.session_state.chat_error = "Rate limit exceeded. Please wait a moment and try again."
        except groq.AuthenticationError:
            st.session_state.chat_error = "Invalid API key. Verify GROQ_API_KEY in your .env file."
        except groq.APIStatusError as e:
            st.session_state.chat_error = f"API error {e.status_code}: {e.response.text if hasattr(e.response, 'text') else e}"
        except Exception as e:
            st.session_state.chat_error = f"Unexpected error: {e}"


def clear_callback():
    st.session_state.history = []
    st.session_state.chat_error = ""
    st.session_state.question_input = ""


col1, col2 = st.columns(2)
with col1:
    st.button("Ask", on_click=ask_callback)
with col2:
    st.button("Clear conversation", on_click=clear_callback)

if not API_KEY:
    st.error("Missing GROQ_API_KEY. Add it to the `.env` file and restart the app.")

if st.session_state.chat_error:
    st.error(st.session_state.chat_error)

if st.session_state.history:
    st.markdown("---")
    st.subheader("Conversation")
    for entry in reversed(st.session_state.history):
        st.markdown(f"**You:** {entry['question']}")
        st.markdown(f"**AI:** {entry['answer']}")
        st.markdown("---")

st.markdown(
    "---\n"
    "**Tips:** Use clear, simple questions. If the answer is incomplete, try rephrasing or ask follow-up questions."
)
