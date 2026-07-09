import pickle

class VectorStore:

    def __init__(self):
        self.data =[]

    def add(
            self,
            embedding,
            metadata,
    ):
        self.data.append(
            {
                "embedding":embedding,
                "metadata":metadata
            }
        )
    
    def get_all(self):

        return self.data
    
    def save(self, file_path):
        with open(file_path,"wb") as f:
            pickle.dump(self.data,f)

    def load(self, file_path):
        with open(file_path,"rb") as f:
            self.data=pickle.load(f)

    def has_source(self, source):

        for item in self.data:
            name = item["metadata"]["name"]
            if name == source:
                return True
        return False