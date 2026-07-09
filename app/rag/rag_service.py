from app.rag.embedder import PDFEmbedder
from app.rag.retriever import Retriever
from app.llm.client import OLLAMAClient
from app.rag.embedder import CodeEmbedder


class PDFRAGService:

    def __init__(
        self,
        vector_store
    ):

        self.embedder = PDFEmbedder()

        self.retriever = Retriever()

        self.vector_store = vector_store

        self.llm=OLLAMAClient()

    def retrieve_context(
        self,
        question,
        history,
        k=7
    ):

        rewritten_query=(self.llm.rewrite_query(
                          history,
                          question
                          )
                        )

        query_embedding = (
            self.embedder.embed(
                rewritten_query
            )
        )

        results = (
            self.retriever.retrieve(
                query_embedding,
                self.vector_store,
                k
            )
        )

        context = ""

        for score, item in results:

            context += (
                item["metadata"]["content"]
                + "\n\n"
            )

        return context
    

#=------------------------------------------------------------------------------------------------------------

class CODERAGService:

    def __init__(
        self,
        vector_store
    ):

        self.embedder = CodeEmbedder()

        self.retriever = Retriever()

        self.vector_store = vector_store

        self.llm=OLLAMAClient()

    def retrieve_context(
        self,
        question,
        history,
        k=7
    ):

        rewritten_query=(self.llm.rewrite_query(
                          history,
                          question
                          )
                        )

        query_embedding = (
            self.embedder.embed(
                rewritten_query
            )
        )

        results = (
            self.retriever.retrieve(
                query_embedding,
                self.vector_store,
                k
            )
        )

        context = ""

        for score, item in results:

            context += (
                item["metadata"]["content"]
                + "\n\n"
            )

        return context