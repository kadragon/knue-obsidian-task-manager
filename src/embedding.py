import os
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


def get_cached_embedder(model="text-embedding-3-small", cache_dir="./.cache/"):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    embedding = OpenAIEmbeddings(
        model=model, openai_api_key=os.getenv("OPEN_AI_API"))
    store = LocalFileStore(cache_dir)

    try:
        cached_embedder = CacheBackedEmbeddings.from_bytes_store(
            underlying_embeddings=embedding,
            document_embedding_cache=store,
            namespace=embedding.model,
        )

        # 캐시 사용 여부를 확인하는 함수 추가
        def is_cached(text):
            original_hits = cached_embedder.cache_hits
            _ = cached_embedder.embed_documents([text])
            return cached_embedder.cache_hits > original_hits

        # is_cached 함수를 cached_embedder에 추가
        cached_embedder.is_cached = is_cached

    except Exception as e:
        print(f"Failed to create cached embedder: {e}")
        raise

    return cached_embedder
