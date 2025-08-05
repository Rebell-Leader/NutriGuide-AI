import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.vector_store_manager import VectorStoreManager

def create_rag_chain(vector_store_manager: VectorStoreManager, model_name: str = "gpt-3.5-turbo", threshold: float = 0.75):
    """
    Creates the RAG chain with a fallback mechanism.

    Args:
        vector_store_manager: An instance of the VectorStoreManager class.
        model_name: The name of the OpenAI model to use.
        threshold: The similarity threshold for the fallback mechanism.

    Returns:
        A LangChain runnable.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # RAG prompt
    rag_prompt_template = """
    You are a helpful nutrition assistant for people with diabetes. Answer the user's question based ONLY on the following context.

    Context: {context}

    Question: {question}

    Answer:
    """
    rag_prompt = ChatPromptTemplate.from_template(rag_prompt_template)

    # Fallback prompt
    fallback_prompt_template = """
    You are a helpful nutrition assistant for people with diabetes. The user asked a question that you cannot answer based on the available information.
    Politely inform the user that you don't have the information they are looking for and suggest they ask a different question.

    Question: {question}

    Answer:
    """
    fallback_prompt = ChatPromptTemplate.from_template(fallback_prompt_template)

    llm = ChatOpenAI(model_name=model_name, api_key=api_key)

    def retrieve_context(query: str):
        return vector_store_manager.search(query, top_k=1)

    def context_is_sufficient(docs):
        if not docs:
            return False
        return docs[0][1] >= threshold

    # The RAG chain for when context is sufficient
    rag_chain_main = (
        (lambda x: {"context": x["context"][0][0]['answer'], "question": x["question"]})
        | rag_prompt
        | llm
        | StrOutputParser()
        | (lambda x: {"response": x, "source_used": True})
    )

    # The fallback chain
    fallback_chain = (
        fallback_prompt
        | llm
        | StrOutputParser()
        | (lambda x: {"response": x, "source_used": False})
    )

    # The final chain with the branch
    rag_chain = (
        {"context": retrieve_context, "question": RunnablePassthrough()}
        | RunnableBranch(
            (lambda x: context_is_sufficient(x["context"]), rag_chain_main),
            fallback_chain,
        )
    )

    return rag_chain
