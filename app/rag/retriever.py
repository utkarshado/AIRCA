import numpy as np

class Retriever:
    def cosine_similarity(self,vA,vB):
        return np.dot(vA,vB)/(np.linalg.norm(vA)*np.linalg.norm(vB))
    

    def retrieve(self,query_embedding,vector_store,k=3):
        scores=[]

        for item in  vector_store.get_all():
            score=self.cosine_similarity(
                query_embedding,
                item["embedding"],
            )

            scores.append(
                (
                    score,
                    item,
                )
            )
        
        scores.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return scores[:k]