from dotenv import load_dotenv
load_dotenv()

import os
from openai import OpenAI

while True:
    message = str(input("Ask ChatGPT: "))

    if message=="exit": break

    client = OpenAI(
        api_key=os.environ.get("OPEN_API_KEY"),
    )

    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'user',
                'content': message,
            }
        ],
    )

    print()
    print(completion.choices[0].message.content)
    # print(completion.created)
    # for comp in completion.choices:
    #     print(comp.message)
    #     print(comp.message.content)
    #     print(comp.message.role)
    #     print(comp.message.tool_calls)
    #     print(comp.finish_reason)
    print()