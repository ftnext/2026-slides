# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "litellm",
# ]
# ///
from litellm import completion

messages = [
    {
        "role": "system",
        "content": "ユーザーの入力する日本語のテキストを英語に翻訳してください",
    },
    {
        "role": "user",
        "content": "プロデューサーの同僚の皆さん、みりっほー！ 仕掛け人モード にっPです",
    },
]

for model in ["openai/gpt-5.6-luna", "gemini/gemini-3.7-flash"]:
    print(f"{model=}")
    response = completion(model=model, messages=messages)
    print(response.choices[0].message.content)
    print()
