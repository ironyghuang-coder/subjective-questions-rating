from src.web.dto.docSample import DocSample
from src.agent.vectorMemory import VectorMemory

class VectorService:
    def __init__(self):
        self.long_term_memory = VectorMemory()

    def save_doc_sample(self, doc_sample : DocSample):
        print(doc_sample.model_dump_json())
        customer_metadata = {
            "topic": doc_sample.topic,
            "category": doc_sample.category,
            "score": doc_sample.score,
        }
        doc_sample_memory_id = self.long_term_memory.add_memory(doc_sample,customer_metadata,doc_sample.importance)
        print(f"saved doc sample: {doc_sample_memory_id}")
        return doc_sample_memory_id

    def clean_doc_sample(self, doc_sample_memory_id:str):
        self.long_term_memory.delete_memory(doc_sample_memory_id)

    def clean_all_doc_sample(self):
        memories = self.long_term_memory.get_all_memories()
        deleted_memories = []
        for memory in memories:
            print(memory)
            self.long_term_memory.delete_memory(memory["id"])
            deleted_memories.append(memory)
        return deleted_memories