from zai import ZhipuAiClient

client = ZhipuAiClient(
    api_key="bd09ca3266fb4d63a2aeaccecf6fa411.6GCQ3TJ2IiFE8yc6"
)  # 填写您自己的 APIKey
response = client.chat.completions.create(
    model="glm-4.5v",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "file_url",
                    "file_url": {
                        "url": "https://cdn.bigmodel.cn/static/demo/demo2.txt"
                    },
                },
                {
                    "type": "file_url",
                    "file_url": {
                        "url": "https://cdn.bigmodel.cn/static/demo/demo1.pdf"
                    },
                },
                {"type": "text", "text": "What are the files show about?"},
            ],
        }
    ],
    thinking={"type": "enabled"},
)
print(response.choices[0].message)
