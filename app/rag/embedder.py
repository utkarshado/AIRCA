from sentence_transformers import SentenceTransformer

class BaseEmbedder:
    def embed(self,text):
        raise NotImplementedError

class PDFEmbedder(BaseEmbedder):

    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    #def embed(self,text):
    #    response=(
    #        self.client.models.embed_content(
    #            model="gemini-embedding-001",
    #            contents=text
    #            )
    #        )
    #   return response.embeddings[0].values

    def embed(self, text):
        response=(
            self.model.encode(text, normalize_embeddings=True)
        )

        return response
    
class CodeEmbedder(BaseEmbedder):

    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    def embed(self, text):
        response=(
            self.model.encode(text, normalize_embeddings=True)
        )

        return response
