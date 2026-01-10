from langchain_ollama import ChatOllama

from app.core.config import settings

if __name__ == "__main__":
    llm = ChatOllama(
        model="qwen3:8b",
        # base_url="http://localhost:11434",
        # timeout=300,  # 增加超时时间到 300 秒
        # num_ctx=2048,  # 限制上下文长度，减少内存压力
    )

    messages = [
        (
            "system",
            "You are a helpful assistant that translates English to French. Translate the user sentence.",
        ),
        ("human", "I love programming."),
    ]
    ai_msg = llm.invoke(messages)
    print(ai_msg)
    # import ollama
    #
    # if __name__ == "__main__":
    #     response = ollama.chat(
    #         model='qwen3:8b',
    #         messages=[
    #             {'role': 'user', 'content': 'Hello, how are you?'}
    #         ]
    #     )
    #     print(response['message']['content'])
