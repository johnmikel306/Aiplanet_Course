import streamlit as st
from beyondllm import source, retrieve, embeddings, llms, generator
from beyondllm.memory import ChatBufferMemory
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    st.title("RAG Pipeline with BeyondLLM")

    # Set up environment variables
    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

    # Initialize the source
    data = source.fit(path="https://youtu.be/Mmx0ewVl2ks", dtype="url", chunk_size=512, chunk_overlap=100)

    # Initialize memory with a specified window size
    memory = ChatBufferMemory(window_size=3)  # Retains the last three interactions

    embed_model = embeddings.GeminiEmbeddings(api_key=os.environ['GOOGLE_API_KEY'], model_name="models/embedding-001")

    retriever = retrieve.auto_retriever(
        data=data, 
        embed_model=embed_model, 
        type="normal", 
        top_k=5,
        memory=memory
    )

    llm = llms.GeminiModel(model_name="gemini-pro", google_api_key=os.environ['GOOGLE_API_KEY'])

    system_prompt = """You are a Customer support Assistant who answers user query from the given CONTEXT, sound like a customer service
    You are honest, coherent and don't hallucinate
    If the user query is not in context, simply tell `We are sorry, we don't have information on this`
    """

    # User input
    user_query = st.text_input("Enter your question:")

    if st.button("Submit"):
        if user_query:
            pipeline = generator.Generate(question=user_query, system_prompt=system_prompt, retriever=retriever, llm=llm)
            response = pipeline.call()
            st.write("Response:", response)
        else:
            st.write("Please enter a question.")

if __name__ == "__main__":
    main()