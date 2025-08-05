import streamlit as st
from dotenv import load_dotenv
from src.rag_chain import create_rag_chain
from src.vector_store_manager import VectorStoreManager
from src.data_loader import load_faqs
from src.preprocessor import clean_text

# --- App Setup ---
load_dotenv()
st.set_page_config(page_title="NutriGuide-AI", page_icon="🤖")
st.title("🤖 NutriGuide-AI")
st.write(
    "A nutrition chatbot for people with diabetes, powered by AI. "
    "Ask a question below and get an answer from our knowledge base."
)

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a new FAQ JSON file", type="json")
if uploaded_file is not None:
    # Read the uploaded JSON file
    import json
    new_faqs = json.load(uploaded_file)

    # Process the new data
    documents = []
    for faq in new_faqs:
        for question in faq['questions']:
            documents.append({
                'question': clean_text(question),
                'answer': faq['answer']
            })

    # Reset the vector store and ingest new data
    VectorStoreManager.reset_and_ingest(documents)
    st.success(f"Successfully uploaded and processed {len(documents)} questions.")
    # Update the RAG chain to use the new vector store
    rag_chain = create_rag_chain()

# --- Initialization ---
@st.cache_resource
def get_vector_store_manager():
    return VectorStoreManager()

@st.cache_resource
def get_rag_chain():
    # Load and process data
    faqs = load_faqs('data/nutrition_faq.json')
    documents = []
    for faq in faqs:
        for question in faq['questions']:
            documents.append({
                'question': clean_text(question),
                'answer': faq['answer']
            })

    # Ingest into Qdrant
    vector_store_manager = get_vector_store_manager()
    vector_store_manager.ingest_data(documents)
    print(f"Successfully ingested {len(documents)} points into the collection.")
    return create_rag_chain(vector_store_manager)

vector_store_manager = get_vector_store_manager()
rag_chain = get_rag_chain()

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = rag_chain.invoke(prompt)
            # Display the response
            st.markdown(result["response"])
            # Display RAG indication
            if result["source_used"]:
                st.caption("Answer generated using knowledge base.")
            else:
                st.caption("Answer generated without knowledge base (fallback).")
    st.session_state.messages.append({"role": "assistant", "content": result["response"]})
