from langchain.memory import ConversationBufferMemory

# only good until restart
MEMORIES = {}


def getMemory(namespace: str) -> ConversationBufferMemory:
    if namespace not in MEMORIES:
        MEMORIES[namespace] = ConversationBufferMemory(
            memory_key="chat_history",
            input_key="question",
            output_key="answer",
            return_messages=True,
        )
    return MEMORIES[namespace]
