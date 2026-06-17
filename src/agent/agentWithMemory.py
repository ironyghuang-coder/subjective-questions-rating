from src.agent.vectorMemory import VectorMemory
from src.agent.shortTermMemory import ShortTermMemory
from src.agent.brain import AgentBrain

class AgentWithMemory:
    """带有记忆系统的AI Agent"""

    def __init__(self, llm_client):
        self.llm = llm_client
        self.short_term_memory = ShortTermMemory(max_turns=10)
        self.long_term_memory = VectorMemory()

    def process_query(self, user_query):
        """处理用户查询"""

        # 1. 从长期记忆中检索相关信息
        relevant_context = self.long_term_memory.get_relevant_context(user_query)

        # 2. 构建完整的上下文
        short_term_context = self.short_term_memory.get_context()

        # 3. 准备系统提示词
        system_message = "你是一个计算机技术与软件专业技术资格（水平）考试系统架构设计师论文题目评卷专家"
        if relevant_context:
            system_message += f"\n\n相关参考论文：\n{relevant_context}"

        # 4. 调用LLM生成回答
        messages = [{"role": "system", "content": system_message}]
        messages.extend(short_term_context)
        query_content = f"请结合相关论文以及系统架构设计师相关教材点评以下论文并给出得分(满分75分,45分及格):\n{user_query}"
        messages.append({"role": "user", "content": query_content})

        response = self.llm.think(messages)

        # 5. 更新短期记忆
        self.short_term_memory.add_message("user", user_query)
        self.short_term_memory.add_message("assistant", response)


        return response





# 使用示例
if __name__ == "__main__":
    llm_client = AgentBrain()
    # 创建带记忆的Agent
    agent = AgentWithMemory(llm_client)

    with open('D:\\work\\agent\\ai-agent-project\\test_doc\\test1.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 模拟对话
    conversations = [
        lines
    ]

    for query in conversations:
        print(f"\n用户: {query}")
        response = agent.process_query(query)
        print(f"助理: {response}")
