import chromadb
from sentence_transformers import SentenceTransformer
import uuid
import time
import os


class VectorMemory:
    """基于向量数据库的记忆系统"""

    def __init__(self, persist_directory="./memory_db"):
        # 初始化 embedding 模型
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

        # 初始化 ChromaDB
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="agent_memories",
            metadata={"description": "AI Agent 的长期记忆"}
        )

    def add_memory(self, content, metadata=None, importance=0.5):
        """添加记忆到向量数据库"""

        # 生成 embedding
        embedding = self.embedding_model.encode(content).tolist()

        # 准备元数据
        full_metadata = {
            "timestamp": time.time(),
            "importance": importance,
            "content_length": len(content)
        }
        if metadata:
            full_metadata.update(metadata)

        # 生成唯一ID
        memory_id = str(uuid.uuid4())

        # 添加到数据库
        self.collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[full_metadata],
            ids=[memory_id]
        )

        return memory_id

    def search_memories(self, query, n_results=5, min_similarity=-20):
        """搜索相关记忆"""

        # 生成查询的 embedding
        query_embedding = self.embedding_model.encode(query).tolist()

        # 在向量数据库中搜索
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        # 处理结果
        memories = []
        if results["documents"]:
            for i in range(len(results["documents"][0])):
                similarity = 1 - results["distances"][0][i]  # 转换距离为相似度

                if similarity >= min_similarity:
                    memory = {
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "similarity": similarity,
                        "id": results["ids"][0][i]
                    }
                    memories.append(memory)

        # 按相似度排序
        memories.sort(key=lambda x: x["similarity"], reverse=True)
        return memories

    def get_relevant_context(self, query, max_memories=3):
        """获取与查询相关的记忆作为上下文"""

        memories = self.search_memories(query, n_results=max_memories)

        if not memories:
            return ""

        # 构建上下文字符串
        context_parts = []
        for i, memory in enumerate(memories):
            content = memory["content"]
            similarity = memory["similarity"]
            timestamp = memory["metadata"]["timestamp"]
            if "score" in memory["metadata"]:
                score = memory["metadata"]["score"]
            else:
                score = 0

            # 格式化时间
            time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))

            context_parts.append(
                f"[相关论文 {i+1},相似度:{similarity:.2f}，时间:{time_str},得分:{score}]\n{content}"
            )

        return "\n\n".join(context_parts)

    def delete_memory(self, memory_id):
        """删除记忆"""
        self.collection.delete(ids=[memory_id])

    def get_all_memories(self, limit=100):
        """获取所有记忆（按时间倒序）"""
        # 注意：ChromaDB 没有直接的获取所有功能
        # 这里通过搜索一个通用查询来获取
        results = self.collection.query(
            query_embeddings=[self.embedding_model.encode(" ").tolist()],  # 空查询
            n_results=limit
        )

        memories = []
        if results["documents"]:
            for i in range(len(results["documents"][0])):
                memory = {
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "id": results["ids"][0][i]
                }
                memories.append(memory)

        # 按时间倒序排序
        memories.sort(key=lambda x: x["metadata"]["timestamp"], reverse=True)
        return memories

    def read_files_to_memories(self, directory, category, score):
        customer_metadata = {
            "category": category,
            "score": score
        }
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                    content = file.read()
                    print(content, end='\n')
                    memory_id = self.add_memory(content,customer_metadata)
                    print('add memory_id:' + memory_id)


if __name__ == "__main__":
    long_term_memory = VectorMemory()
    memories = long_term_memory.get_all_memories()
    for memory in memories:
        print(memory)
        long_term_memory.delete_memory(memory["id"])

    long_term_memory.read_files_to_memories('D:\\work\\agent\\ai-agent-project\\data_doc','系统架构设计师', 75)