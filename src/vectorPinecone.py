from pinecone import Pinecone, ServerlessSpec
from src.embedding import get_cached_embedder
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()


class VectorDatabasePinecone:
    def __init__(self, index_name: str = "task-manager-index"):
        self.index_name = index_name
        self.embedder = get_cached_embedder()
        self.pc = Pinecone(os.getenv("PINECONE_API_KEY"))
        self.index = self._get_index()

    def _create_index(self):
        self.pc.create_index(
            self.index_name, dimension=1536, metric="cosine", spec=ServerlessSpec(
                region="us-east-1",
                cloud="aws"
            )
        )

    def _get_index(self):
        return self.pc.Index(self.index_name)

    def _generate_id(self, content):
        return hashlib.md5(content.encode()).hexdigest()

    def upsert(self, file_path):
        filename = '10_WorkNotes' + \
            file_path.replace(os.getenv('OBSIDIAN_DIR'), '')

        with open(file_path, "r", encoding="utf-8") as file:
            content = ''.join(file.read().split("---")[2:])

            self.index.upsert(
                vectors=[
                    {
                        "id": self._generate_id(filename.split("/")[-1]),
                        "values": self.embedder.embed_query(content),
                        "metadata": {"source": filename, "content": content}
                    }
                ],
                namespace="test"
            )

    def query(self, namespace: str, query: str):
        query_vector = self.embedder.embed_query(query)
        query_response = self.index.query(
            namespace=namespace,
            vector=query_vector,
            top_k=2,
            include_values=True,
            include_metadata=True
        )
        return query_response


if __name__ == "__main__":
    vdp = VectorDatabasePinecone()

    # filename = "/등록/출력물관리/202409_등록내역확인_고지서출력에서_현재학기_고지서가_안보임/_등록내역확인 고지서출력에서 현재학기 고지서가 안보임.md"

    folder_path = os.getenv('OBSIDIAN_DIR') + '/전임교원공채/'

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.md'):
                filename = os.path.join(root, file)
                # print(filename)
                vdp.upsert(filename)

    # result = vdp.query(namespace="test", query="등록금 고지서 납부확인서")

    # for r in result.matches:
    #     data = r.metadata['source']
    #     make_markdown = f'[[{data[:-3]}]]'

    #     print(make_markdown, '\n', r.metadata['content'])
