from app.rag.loaders.pdf_loader import PDFLoader
from app.rag.chunkers.pdf_chunker import PDFChunker
from app.rag.embedder import PDFEmbedder
from app.rag.vector_store import VectorStore
import os
#-------------------------------------------------------------------------------------------------
from app.rag.loaders.code_loader import CodeLoader
from app.rag.chunkers.code_chunker import CodeChunker
from app.rag.embedder import CodeEmbedder

class PDFIngestor:

    def __init__(self):

        self.loader = PDFLoader()

        self.chunker = PDFChunker()

        self.embedder = PDFEmbedder()

    def ingest(self, pdf_path, store_path, source_name= None):

        source = source_name if source_name else pdf_path
        if os.path.exists(store_path):
            vector_store=VectorStore()

            vector_store.load(store_path)
            print("Loaded existing Vectore Store Database .")
            
            if vector_store.has_source(source):
                print("PDF already ingested.")

                return vector_store

        else:
            vector_store=VectorStore()

        text = self.loader.load(
            pdf_path
        )

        chunks = self.chunker.chunk(
            text
        )

        for i, chunk in enumerate(chunks):

            embedding = (
                self.embedder.embed(
                    chunk
                )
            )

            vector_store.add(
                embedding,
                {
                    "type": "pdf",
                    "name": source,
                    "path": pdf_path,
                    "content": chunk
                }
            )

        vector_store.save(store_path)
        print("Created and Saved Vector DB .")

        return vector_store
    
#--------------------------------------------------------------------------------------------------------

class CodeIngestor:

    def __init__(self):
        
        self.loader = CodeLoader()

        self.chunker = CodeChunker()

        self.embedder = CodeEmbedder()

    def ingest(self, project_path, store_path):
        if os.path.exists(store_path):
            vector_store=VectorStore()

            vector_store.load(store_path)
            print("Loaded existing Vectore Store Database .")
            if vector_store.has_source(project_path):
                print("Codebase already ingested.")

            return vector_store

        else:
            vector_store=VectorStore()

        code=self.loader.load(project_path)

        chunks= self.chunker.chunk(code)
        
        for chunk in chunks:
            embedding = (
                self.embedder.embed(
                    chunk["content"]
                )
            )

            vector_store.add(
                embedding, chunk
            )

        vector_store.save(store_path)
        print("Created and Saved Vector DB .")

        return vector_store