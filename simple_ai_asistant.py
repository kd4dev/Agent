from openai import OpenAI
import json
from tools import get_current_time, FUNCTION_NAME_TO_FUNCTION_MAP, TOOLS
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []
messages.append({
    "role": "system",
    "content": "You are a helpful and humble AI assistant. When a query requires multiple steps or tools, call the tools sequentially step-by-step before providing your concise final answer."
})

while True:
    user_input = input("\nKedar: ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    max_steps = 5

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS
        )

        msg = response.choices[0].message

        if not msg.tool_calls:
            break

        messages.append(msg.model_dump(exclude_none=True))

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name

            try:
                func_args = json.loads(
                    tool_call.function.arguments or "{}"
                )

                print(f"  [Tool Chain Step {step + 1}] Calling {func_name}({tool_call.function.arguments.strip()})...")
                fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
                result = fn(**func_args)
                print(f"  [Tool Result] {result}")

            except Exception as e:
                result = f"Error while running {func_name}: {e}"
                print(f"  [Tool Error] {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    else:
        fallback = "Sorry, I couldn't finish this within the step limit."

        messages.append({
            "role": "assistant",
            "content": fallback
        })

        print("Assistant:", fallback)
        continue

    messages.append({
        "role": "assistant",
        "content": msg.content or ""
    })

    print("Assistant:", msg.content or "")