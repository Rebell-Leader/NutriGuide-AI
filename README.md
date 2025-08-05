# NutriGuide-AI

NutriGuide-AI is a nutrition chatbot for people with diabetes, powered by AI. It uses a Retrieval-Augmented Generation (RAG) architecture to answer nutrition-related questions based on a predefined FAQ dataset.

## System Architecture: RAG Pipeline

The chatbot is built using a RAG (Retrieval-Augmented Generation) pipeline. Here's a visual representation of the architecture:

```mermaid
graph TD
    subgraph User Interface Streamlit
        A[User Input: "What are good snacks?"] --> B{Query Preprocessing};
    end

    subgraph RAG Pipeline
        B --> C[1. Embed Query];
        C --> D[2. Semantic Search in Qdrant];
        D --> E[3. Retrieve Relevant FAQ];
        E --> F[4. Construct Prompt];
        F --> G[5. Query LLM];
    end

    subgraph Backend
        H[FAQ Dataset: nutrition_faq.json] --> I{Data Loading & Chunking};
        I --> J[Embed & Ingest];
        J --> K((Qdrant Vector Store));
        D --> K;
        G --> L[LLM Inference Endpoint];
    end

    G --> M[6. Generate Response];
    M --> N[Display Answer];
    A --> N;

    style K fill:#f9f,stroke:#333,stroke-width:2px
    style L fill:#ccf,stroke:#333,stroke-width:2px
```

## How to Run

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/NutriGuide-AI.git
    cd NutriGuide-AI
    ```

2.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your OpenAI API key:**

    Create a `.env` file in the root of the project and add your OpenAI API key as follows:

    ```
    OPENAI_API_KEY=your-api-key
    ```

4.  **Run the Streamlit app:**

    Run the following command from the root of the project:

    ```bash
    python -m streamlit run src/app.py
    ```

## Project Structure

```
/home/obi/NutriGuide-AI/
|-- data/
|   `-- nutrition_faq.json
|-- notebooks/
|-- src/
|   |-- __init__.py
|   |-- app.py
|   |-- data_loader.py
|   |-- preprocessor.py
|   |-- rag_chain.py
|   `-- vector_store_manager.py
|-- tests/
|-- .env
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Assumptions and Trade-offs

*   **In-memory Vector Store:** For simplicity, the app uses an in-memory Qdrant vector store with `fastembed`. This means that the data is not persisted and needs to be re-ingested every time the app starts. For a production environment, a persistent Qdrant instance (e.g., using Docker or Qdrant Cloud) would be more appropriate.
*   **Embedding Model:** The app uses the `BAAI/bge-small-en-v1.5` model from `fastembed` for creating embeddings. This is a good general-purpose model, but for a production environment, it might be beneficial to fine-tune a model on a domain-specific dataset.
*   **OpenAI API:** The app uses the OpenAI API for the language model. You will need to provide your own API key in a `.env` file to run the app. The model can be easily swapped out for a different one by modifying the `rag_chain.py` file.
*   **Static Knowledge Base:** The chatbot's knowledge is limited to the provided FAQ dataset. To expand its knowledge, you can add more data to the `nutrition_faq.json` file or integrate other data sources.
*   **No Conversation Memory:** The chatbot does not remember previous turns in the conversation. Each query is treated independently. For a more natural conversational flow, a memory component could be added to the RAG chain.
*   **Fallback Behavior:** The chatbot uses a similarity threshold to determine if a relevant answer can be found in the knowledge base. If the similarity score of the retrieved document is below the threshold (currently set to 0.75), the chatbot will use a separate prompt to generate a more natural-sounding fallback message. This is implemented using a `RunnableBranch` in the RAG chain. This threshold can be adjusted in the `rag_chain.py` file.
*   **Dynamic Knowledge Base:** The application supports uploading a new FAQ JSON file at any time, which will reset the vector store and ingest the new dataset.
