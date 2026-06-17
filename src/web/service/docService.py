from src.web.dto.docItem import DocItem
from src.agent.brain import AgentBrain
from src.agent.agentWithMemory import AgentWithMemory

class DocService:

    def __init__(self):
        self.llm_client = AgentBrain()
        self.agent = AgentWithMemory(self.llm_client)

    def send_doc_item(self, doc_Item:DocItem):
        print(doc_Item.model_dump_json())
        query = doc_Item.topic + '\n' + doc_Item.content
        response = self.agent.process_query(query)
        print(f"助理: {response}")
        return response