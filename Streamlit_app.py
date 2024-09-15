import streamlit as st
from beyondllm import source, retrieve, embeddings, llms, generator
from beyondllm.memory import ChatBufferMemory
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import time

# Load environment variables from .env file
load_dotenv()

# Caching the embedding model to avoid re-initialization
@st.cache_resource
def load_embedding_model(api_key):
    return embeddings.GeminiEmbeddings(api_key=api_key, model_name="models/embedding-001")

# Caching the LLM model to avoid re-initialization
@st.cache_resource
def load_llm(api_key):
    return llms.GeminiModel(model_name="gemini-pro", google_api_key=api_key)

# Caching the source data for faster access if it's already loaded
@st.cache_data
def fetch_source_data(path, chunk_size, chunk_overlap):
    return source.fit(path=path, dtype="url", chunk_size=chunk_size, chunk_overlap=chunk_overlap)

def main():
    st.title("RAG Pipeline with BeyondLLM")

    # Set up environment variables
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        st.error("GOOGLE_API_KEY not found. Please make sure it's set in the .env file.")
        return  # Exit if the API key is missing

    # Start loading models in parallel to speed up initialization
    with ThreadPoolExecutor() as executor:
        future_embed_model = executor.submit(load_embedding_model, google_api_key)
        future_llm_model = executor.submit(load_llm, google_api_key)
    
    # Load source data (cached for speed if already processed)
    # st.info("Loading video data...")
    start_time = time.time()
    data = fetch_source_data(path="https://youtu.be/Mmx0ewVl2ks", chunk_size=512, chunk_overlap=50)
    # st.success(f"Video data loaded in {time.time() - start_time:.2f} seconds.")

    # Initialize memory with a specified window size
    memory = ChatBufferMemory(window_size=3)  # Retains the last three interactions

    # Fetch models from futures
    embed_model = future_embed_model.result()
    llm_model = future_llm_model.result()

    retriever = retrieve.auto_retriever(
        data=data, 
        embed_model=embed_model, 
        type="normal", 
        top_k=3,  # Reduced top_k to make retrieval faster
        memory=memory
    )

    system_prompt = """You are a Customer support Assistant who answers user query from the given CONTEXT, sound like a customer service
    You are honest, coherent and don't hallucinate
    If the user query is not in context, simply tell `We are sorry, we don't have information on this`
    """

    # User input
    user_query = st.text_input("Enter your question:")

    if st.button("Submit"):
        if user_query:
            # Generate the response
            # st.info("Generating response...")
            pipeline = generator.Generate(question=user_query, system_prompt=system_prompt, retriever=retriever, llm=llm_model)
            start_time = time.time()
            response = pipeline.call()
            st.write("Response:", response)
            # st.success(f"Response generated in {time.time() - start_time:.2f} seconds.")
        else:
            st.write("Please enter a question.")

if __name__ == "__main__":
    main()
