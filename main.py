import os
import openai


def get_image_files(directory):
    exts = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.splitext(f)[1].lower() in exts
    ]


def call_openai_ocr(index, api_key):
    openai.base_url = "https://api.siliconflow.cn/v1"
    openai.api_key = api_key
    # 构造三位数编号，例如 001、002、003……
    index_str = f"{index:03d}"

    # 使用 GitHub raw 链接
    image_url = f"https://raw.githubusercontent.com/RaptorValley/OCR-GuiBianShu-TEMP/main/pages_{index_str}.jpg"
    print(image_url)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                        "detail": "auto",
                    },
                }
            ],
        }
    ]

    response = openai.chat.completions.create(
        model="deepseek-ai/deepseek-ocr",
        messages=messages,
    )
    return response.choices[0].message.content


def save_to_md(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    api_key = "sk-qqihqjrfuqkoxxxqmvcxddazqfroocdhmjptkazjgetbvqcf"  # 请设置你的API KEY
    output_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, 177):  # 从 001 到 176
        print(f"正在处理第 {i:03d} 张图片...")
        text = call_openai_ocr(i, api_key)
        md_path = os.path.join(output_dir, f"{i:03d}.md")
        save_to_md(text, md_path)
        print(f"已保存：{md_path}")


if __name__ == "__main__":
    main()
