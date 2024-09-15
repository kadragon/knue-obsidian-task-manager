from pinecone import Pinecone, ServerlessSpec
from src.embedding import get_cached_embedder
import os
import time
from datetime import datetime, timedelta
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
                        "id": self._generate_id(filename.split("/")[-2]),
                        "values": self.embedder.embed_query(content),
                        "metadata": {"source": filename, "content": content}
                    }
                ],
                namespace="test"
            )

    def _find_recent_md_files(self, folder_path):
        # 현재 시간에서 1주일 전 시간 계산
        one_week_ago = datetime.now() - timedelta(days=3)

        recent_files = []

        # 폴더 내 모든 파일 순회
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    # 파일의 최종 수정 시간 확인
                    mod_time = os.path.getmtime(file_path)
                    mod_datetime = datetime.fromtimestamp(mod_time)

                    # 최근 1주일 내에 수정된 파일인지 확인
                    if mod_datetime > one_week_ago:
                        recent_files.append(file_path)

        return recent_files

    def upsert_recent(self):
        recent_files = self._find_recent_md_files(os.getenv('OBSIDIAN_DIR'))

        for file in recent_files:
            print(file)
            self.upsert(file)

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

    def get_reference(text, type='source'):
        result = self.query(namespace="test", query=text)

        if type == 'source':
            reference = '\n'.join(
                [f'- [[{r.metadata['source']}]]' for r in result.matches])

        elif type == 'content':
            reference = ''.join([r.metadata['content']
                                for r in result.matches])
        return reference


if __name__ == "__main__":
    vdp = VectorDatabasePinecone()

    folder_path = os.getenv('OBSIDIAN_DIR')

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.md'):
                filename = os.path.join(root, file)
                print(filename)
                vdp.upsert(filename)
