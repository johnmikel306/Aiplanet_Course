import streamlit as st
import os
import tempfile

# Configure NLTK data path for Streamlit Cloud
import nltk
nltk_data_dir = os.path.join(tempfile.gettempdir(), 'nltk_data')
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir=nltk_data_dir, quiet=True)
    nltk.download('punkt_tab', download_dir=nltk_data_dir, quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', download_dir=nltk_data_dir, quiet=True)

# Now import beyondllm after NLTK is configured
from beyondllm import source, retrieve, embeddings, llms, generator

# Page configuration
st.set_page_config(
    page_title="Simple RAG Chat",
    page_icon="🤖",
    layout="centered"
)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "retriever" not in st.session_state:
        st.session_state.retriever = None
    if "llm" not in st.session_state:
        st.session_state.llm = None
    if "initialized" not in st.session_state:
        st.session_state.initialized = False

def setup_rag_pipeline(api_key, source_type, source_input, uploaded_file=None):
    """Set up the RAG pipeline"""
    try:
        os.environ['GOOGLE_API_KEY'] = api_key
        
        with st.spinner("🔄 Loading your content..."):
            # Handle different source types
            if source_type == "YouTube Video":
                data = source.fit(
                    path=source_input, 
                    dtype="youtube", 
                    chunk_size=512, 
                    chunk_overlap=50
                )
            else:  # File upload
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Determine file type
                file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                if file_extension == '.pdf':
                    dtype = "pdf"
                elif file_extension in ['.txt', '.md']:
                    dtype = "txt"
                elif file_extension in ['.doc', '.docx']:
                    dtype = "docx"
                else:
                    dtype = "txt"
                
                data = source.fit(
                    path=tmp_path, 
                    dtype=dtype, 
                    chunk_size=512, 
                    chunk_overlap=50
                )
                
                # Clean up temp file
                os.unlink(tmp_path)
        
        with st.spinner("🔄 Setting up AI models..."):
            # Initialize embeddings and retriever
            embed_model = embeddings.GeminiEmbeddings(
                api_key=api_key, 
                model_name="models/embedding-001"
            )
            
            retriever = retrieve.auto_retriever(
                data=data, 
                embed_model=embed_model, 
                type="normal", 
                top_k=5
            )
            
            # Initialize LLM
            llm = llms.GeminiModel(
                model_name="gemini-2.5-flash-lite", 
                google_api_key=api_key
            )
        
        st.session_state.retriever = retriever
        st.session_state.llm = llm
        st.session_state.initialized = True
        st.success("✅ Ready to chat!")
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.session_state.initialized = False

def main():
    st.title("🤖 Simple RAG Chat")
    
    initialize_session_state()
    
    # Setup section - only show if not initialized
    if not st.session_state.initialized:
        st.markdown("### 📝 Setup")
        
        # API Key input
        api_key = st.text_input(
            "Google API Key", 
            type="password",
            help="Get your free API key from https://makersuite.google.com/app/apikey"
        )
        
        # Source type selection
        source_type = st.radio(
            "Choose your content source:",
            ["YouTube Video", "Upload File"],
            horizontal=True
        )
        
        # Input based on source type
        if source_type == "YouTube Video":
            youtube_url = st.text_input(
                "YouTube URL",
                placeholder="https://www.youtube.com/watch?v=..."
            )
            uploaded_file = None
        else:
            youtube_url = None
            uploaded_file = st.file_uploader(
                "Upload your file",
                type=['pdf', 'txt', 'md', 'doc', 'docx'],
                help="Supported formats: PDF, TXT, MD, DOC, DOCX"
            )
        
        # Initialize button
        if st.button("🚀 Start Chat", type="primary"):
            if not api_key:
                st.error("⚠️ Please enter your Google API Key")
            elif source_type == "YouTube Video" and not youtube_url:
                st.error("⚠️ Please enter a YouTube URL")
            elif source_type == "Upload File" and not uploaded_file:
                st.error("⚠️ Please upload a file")
            else:
                source_input = youtube_url if source_type == "YouTube Video" else None
                setup_rag_pipeline(api_key, source_type, source_input, uploaded_file)
        
        # Show example
        with st.expander("ℹ️ How to use"):
            st.markdown("""
            1. **Get API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to get a free API key
            2. **Choose Source**: Select YouTube video or upload a file
            3. **Start Chat**: Click the button to initialize
            4. **Ask Questions**: Chat with your content!
            """)
    
    else:
        # Chat interface
        st.markdown("---")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your content..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        system_prompt = """You are a helpful assistant. Answer questions based on the provided context.
                        If you don't know the answer, say so. Be concise and accurate."""
                        
                        pipeline = generator.Generate(
                            question=prompt,
                            system_prompt=system_prompt,
                            retriever=st.session_state.retriever,
                            llm=st.session_state.llm
                        )
                        response = pipeline.call()
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.error(error_msg)
        
        # Reset button in sidebar
        with st.sidebar:
            st.markdown("### 🔧 Controls")
            if st.button("🔄 Start Over"):
                st.session_state.clear()
                st.rerun()
            
            st.markdown("---")
            st.markdown(f"**Messages:** {len(st.session_state.messages)}")

if __name__ == "__main__":
    main()
