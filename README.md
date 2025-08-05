# NutriGuide-AI

Your personal AI-powered nutrition assistant, providing safe and reliable dietary guidance for individuals managing diabetes.

1. Overview of the Approach

NutriGuide AI is a chatbot designed to provide 24/7 nutritional support to people with diabetes. It is built using a Retrieval-Augmented Generation (RAG) architecture to ensure that all responses are grounded in a vetted, medically-sound knowledge base.

The core workflow is as follows:

    Knowledge Ingestion: A structured FAQ dataset (nutrition_faq.json) is processed, and each question-answer pair is converted into a numerical vector (embedding). These embeddings are stored in a Qdrant vector database.

    Semantic Retrieval: When a user asks a question, the system embeds the query and uses semantic search to find the most relevant question-answer pair from the vector database. A similarity score threshold is used to ensure only relevant information is retrieved.

    Augmented Generation: The retrieved answer serves as the context for a Large Language Model (LLM). The LLM then generates a conversational, easy-to-understand response based only on this verified information.

This two-step process combines the factual accuracy of a database with the natural language capabilities of an LLM, making it a safe and effective solution for health-related queries.
2. Integration with Other Systems (e.g., Patient App)

While this prototype is a standalone Streamlit application, it is designed for easy integration into a broader healthcare ecosystem. The core chatbot logic can be containerized using Docker and exposed via a REST API (using a framework like FastAPI).

This microservice architecture allows a patient-facing mobile or web application to simply call the API endpoint with a user's query and receive a response. This has several advantages:

    Centralized Logic: The complex AI/NLP logic is maintained in one place, making updates and improvements seamless.

    Scalability: The service can be scaled independently based on demand.

    Platform Agnostic: Any client (iOS, Android, Web) that can make an HTTP request can integrate the chatbot's functionality.

3. How to Run the Chatbot

[TBD: Final paths and commands will be updated upon project completion]

    Clone the Repository:

    git clone <repository_url>
    cd NutriGuide-AI

    Set Up Environment & Dependencies:
    Create a Python virtual environment and install the required packages.

    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt

    Start Qdrant Vector Store:
    The easiest way to run Qdrant is with Docker.

    docker run -p 6333:6333 qdrant/qdrant

    Ingest Data into Qdrant:
    Run the one-time script to populate the vector database with the FAQ data.

    python ingest.py

    Run the Streamlit Application:

    streamlit run app.py

    You can now access the chatbot in your web browser at http://localhost:8501.

4. Assumptions and Trade-Offs

    Assumption: The initial nutrition_faq.json file is considered the "source of truth" and is assumed to be medically accurate and sufficient for the prototype's scope.

    Trade-Off (Safety vs. Scope): We prioritize safety by strictly limiting the bot's responses to its knowledge base. If no confident match is found (below a similarity threshold of 0.75), the bot will state that it cannot answer. This is safer than providing a potentially incorrect or "hallucinated" answer but reduces the chatbot's helpfulness for out-of-scope questions.

    Trade-Off (Speed vs. Specificity): The use of a general-purpose, pre-trained embedding model (all-MiniLM-L6-v2) allows for rapid development. However, it may not capture the nuances of medical and nutritional terminology as effectively as a model fine-tuned on a domain-specific dataset.

5. How to Expand This Project

This prototype serves as a strong foundation. Future enhancements could include:

    Knowledge Base Expansion: Integrating more comprehensive and dynamic data sources, such as medical guidelines, food composition databases, and vetted research articles.

    Conversational Memory: Adding memory to allow for multi-turn conversations and follow-up questions.

    Hybrid Search: Combining the current semantic search with keyword-based search to improve retrieval accuracy for queries containing specific terms.

    Model Fine-Tuning: Fine-tuning the embedding model on a larger, curated corpus of diabetes-related text to improve its domain understanding.

    Advanced RAG: Implementing techniques like query rewriting or re-ranking retrieved results to enhance the quality of the context provided to the LLM.

6. Monitoring the System in Production

To ensure the chatbot remains effective and safe in a production environment, we would implement a multi-faceted monitoring strategy:

    Performance Logging: Log key data for every query: the user's question, the retrieved context, the similarity score, and the final LLM-generated answer.

    Gap Analysis: Regularly analyze queries where the retrieval score was below the confidence threshold. These represent gaps in the knowledge base and can guide future content development.

    User Feedback: Incorporate a simple "thumbs up/thumbs down" feedback mechanism in the UI. This direct user feedback is invaluable for identifying inaccurate or unhelpful responses.

    Automated Evaluation: Establish an automated evaluation pipeline (using frameworks like RAGAs) to periodically test the system against a "golden dataset" of questions and expected answers, monitoring for any degradation in performance.
