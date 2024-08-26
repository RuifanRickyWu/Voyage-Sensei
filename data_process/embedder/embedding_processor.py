from CarTravel.data_process.embedder.STEmbedder import STEmbedder

class EmbeddingProcessor:
    _embedder: STEmbedder

    def __init__(self):
        self._embedder = STEmbedder()

    def create_and_load_hotel_embedding(self, name:str, feature: list[str], description: str, reviews: list[str]):
        print("creating emb")
        to_be_converted = [name, description, "".join(feature)]

        for review in reviews:
            to_be_converted.append(review['text'])

        embeddings = []
        for item in to_be_converted:
            try:
                embeddings.append(self._embedder.encode(item))
            except:
                print(name)
                print("something inside it is null")
                print()
        embedding_strings = [','.join(map(str, embedding.flatten())) for embedding in embeddings]
        all_embeddings_str = '|'.join(embedding_strings)

        return all_embeddings_str

    def create_and_load_hotel_embedding_real_time(self, name:str, feature: list[str], description: str, reviews: list[str]):
        to_be_converted = [name, description, "".join(feature)]

        for review in reviews:
            to_be_converted.append(review['text'])

        embeddings = []
        for item in to_be_converted:
            try:
                embeddings.append(self._embedder.encode(item))
            except:
                print("something inside it is null")

        return embeddings

    def create_embedding(self, text: str):
        return self._embedder.encode(text)
