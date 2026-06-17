import time

class ShortTermMemory:
    """短期记忆实现"""

    def __init__(self, max_turns=10):
        self.max_turns = max_turns  # 最大对话轮数
        self.conversation_history = []  # 对话历史
        self.temporary_data = {}  # 临时数据存储

    def add_message(self, role, content):
        """添加消息到对话历史"""
        message = {"role": role, "content": content, "timestamp": time.time()}
        self.conversation_history.append(message)

        # 保持历史不超过最大长度
        if len(self.conversation_history) > self.max_turns:
            self.conversation_history.pop(0)

    def get_context(self):
        """获取对话上下文（用于发送给LLM）"""
        return self.conversation_history[-self.max_turns:]

    def store_temp(self, key, value):
        """存储临时数据"""
        self.temporary_data[key] = value

    def get_temp(self, key, default=None):
        """获取临时数据"""
        return self.temporary_data.get(key, default)

    def clear_temp(self):
        """清除临时数据"""
        self.temporary_data.clear()