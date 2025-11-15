import os
import openai


def get_image_files(directory):
    exts = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.splitext(f)[1].lower() in exts
    ]


def call_openai_ocr(image_path, api_key):
    openai.base_url = "https://api.siliconflow.cn/v1"
    openai.api_key = api_key
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"file:///{image_path}", "detail": "auto"},
                }
            ],
        }
    ]
    # 判断openai库版本，选择不同的API调用方式
    try:
        # openai 1.x 版本
        response = openai.chat.completions.create(
            model="deepseek-ai/DeepSeek-OCR",
            messages=messages,
        )
        return response.choices[0].message.content
    except AttributeError:
        # openai 0.x 版本
        response = openai.ChatCompletion.create(
            model="deepseek-ai/DeepSeek-OCR",
            messages=messages,
        )
        return response["choices"][0]["message"]["content"]


def save_to_md(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    directory = os.path.dirname(__file__)
    api_key = "sk-qqihqjrfuqkoxxxqmvcxddazqfroocdhmjptkazjgetbvqcf"  # 请设置你的API KEY
    image_files = get_image_files(directory)
    for img_path in image_files:
        text = call_openai_ocr(img_path, api_key)
        md_path = os.path.splitext(img_path)[0] + ".md"
        save_to_md(text, md_path)


if __name__ == "__main__":
    main()
