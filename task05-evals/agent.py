import math
from anthropic import Anthropic
from anthropic.types import ToolUseBlock, TextBlock
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────

MODEL = "claude-haiku-4-5-20251001"
SYSTEM_PROMPT = "You are a helpful assistant."

client = Anthropic()

# ── Tool implementations ─────────────────────────────────────────────────────


def get_product(product: str):
    catalog = {
        "jeans": 49.99,
        "shirt": 29.99,
        "dress": 59.99,
        "jacket": 89.99,
        "sneakers": 74.99,
        "hat": 19.99,
        "socks": 9.99,
        "hoodie": 44.99,
        "shorts": 34.99,
        "t-shirt": 24.99,
        "sweater": 54.99,
        "belt": 24.99,
    }
    return catalog[product]


def calculate(op: str, input1: float, input2: float):
    match op:
        case "+":
            return input1 + input2
        case "-":
            return input1 - input2
        case "*":
            return input1 * input2
        case "/":
            return input1 / input2
        case "**":
            return input1**input2


TOOL_REGISTRY = {
    "get_product": get_product,
    "calculate": calculate,
}

# ── Tool specs (sent to Claude) ──────────────────────────────────────────────

GET_PRODUCT_SPEC = {
    "name": "get_product",
    "description": "get_product",
    "input_schema": {
        "type": "object",
        "properties": {
            "product": {
                "type": "string",
                "description": "product",
            },
        },
        "required": ["product"],
    },
}

CALCULATE_SPEC = {
    "name": "calculate",
    "description": "calculator",
    "input_schema": {
        "type": "object",
        "properties": {
            "op": {
                "type": "string",
                "description": "operator",
            },
            "input1": {
                "type": "number",
                "description": "input1",
            },
            "input2": {
                "type": "number",
                "description": "input2",
            },
        },
        "required": ["op", "input1", "input2"],
    },
}

ALL_TOOL_SPECS = [GET_PRODUCT_SPEC, CALCULATE_SPEC]

# ── Agent ─────────────────────────────────────────────────────────────────────


def call_claude(messages, tools, model=None):
    return client.messages.create(
        model=model or MODEL,
        system=SYSTEM_PROMPT,
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )


def execute_tool(name, inputs):
    try:
        return str(TOOL_REGISTRY[name](**inputs))
    except Exception as e:
        return f"Error: {e}"


def run_agent(prompt, eval_mode=False, model=None):
    messages = [{"role": "user", "content": prompt}]
    total_input_tokens = 0
    total_output_tokens = 0

    while True:
        response = call_claude(messages, tools=ALL_TOOL_SPECS, model=model)
        total_input_tokens += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            break

        tool_calls = [
            block for block in response.content if isinstance(block, ToolUseBlock)
        ]

        tool_results = []
        for tool_call in tool_calls:
            result = execute_tool(tool_call.name, tool_call.input)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": result,
                }
            )

        messages.append({"role": "user", "content": tool_results})

    if eval_mode:
        return {
            "messages": messages,
            "usage": {
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
            },
        }

    return "\n".join(
        block.text for block in response.content if isinstance(block, TextBlock)
    )


print("boutique agent ready.")

while True:
    query = input("\nYou: ")
    if not query.strip() or query.strip().lower() in ("quit", "exit", "q"):
        print("Session ended.")
        break
    print(f"\nBoutique: {run_agent(query)}")
