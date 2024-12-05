# RAG Pipeline with BeyondLLM (AI_Planet RAG BootCamp Course)

**RAG Pipeline with BeyondLLM** is a Retrieval-Augmented Generation (RAG) application that utilizes BeyondLLM’s robust capabilities for embedding, retrieval, and language model interaction to provide intelligent responses based on a user-defined context.

---

## Features

- **Retrieval-Augmented Generation (RAG)**:
  Combines document retrieval and AI generation to answer user queries accurately and contextually.
  
- **Source Extraction**:
  Processes and chunks content from URLs or documents.

- **Custom Embeddings**:
  Leverages the `GeminiEmbeddings` model for creating embeddings with fine-tuned similarity search.

- **Retriever System**:
  Efficiently retrieves the most relevant data for a query using `auto_retriever`.

- **LLM Integration**:
  Incorporates Gemini LLM for coherent, customer-service-oriented responses.

- **Session Memory**:
  Implements a chat memory buffer to retain the context of recent user interactions.

---

## Requirements

### API Key
This application requires a **Google API Key** for accessing Gemini models and embeddings. The key should be stored in a `.env` file.

---

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a `.env` file in the root directory with your Google API Key:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## How It Works

1. **Source Extraction**:
   - The app processes content from the provided URL (e.g., YouTube video) using `source.fit`.
   
2. **Embedding Creation**:
   - Generates text embeddings using the Gemini Embeddings API for effective similarity search.

3. **Data Retrieval**:
   - Implements an `auto_retriever` to fetch the most relevant pieces of information based on user queries.

4. **Language Model Interaction**:
   - Utilizes the Gemini LLM for query responses, guided by a customer-support-oriented system prompt.

5. **Chat Memory**:
   - Retains the last three interactions using `ChatBufferMemory` for continuity in multi-turn conversations.

---

## Usage

1. Start the application:
   - Open the app in your browser after running the Streamlit command.

2. Submit a query:
   - Enter a question into the text input field and click **Submit**.

3. Get AI-generated responses:
   - View the customer-support-style response based on the context retrieved from the source data.

4. Interact dynamically:
   - Use follow-up queries, and the memory system will ensure contextual continuity.

---

## Dependencies

- [Streamlit](https://streamlit.io/)
- [BeyondLLM](https://github.com/beyondllm)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)
- Python 3.8+

---

## Contributing

Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.

---

## License

This project is licensed under the MIT License.

---

Explore how RAG pipelines can revolutionize customer support with AI! 🚀
