
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
from typing import List, Dict, Tuple

class VectorStoreManager:
    def __init__(self, collection_name: str = 'nutrition_faqs'):
        self.client = QdrantClient(":memory:")
        self.collection_name = collection_name
        self.embed_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        self._create_collection()

    def _create_collection(self):
        """Creates a new collection, deleting the old one if it exists."""
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )

    def reset_and_ingest(self, documents: List[Dict[str, str]]):
        """Resets the collection and ingests new documents."""
        self._create_collection()
        self.ingest_data(documents)

    def ingest_data(self, documents: List[Dict[str, str]]):
        questions = [doc['question'] for doc in documents]
        question_embeddings = list(self.embed_model.embed(questions))
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=i,
                    vector=embedding,
                    payload={'answer': doc['answer'], 'question': doc['question']}
                )
                for i, (doc, embedding) in enumerate(zip(documents, question_embeddings))
            ],
            wait=True
        )

    def search(self, query: str, top_k: int = 1) -> List[Tuple[Dict, float]]:
        query_embedding = list(self.embed_model.embed(query))[0]
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k
        )
        return [(hit.payload, hit.score) for hit in hits]
