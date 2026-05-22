from openai import OpenAI
import dotenv
import os
import json

dotenv.load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

system_prompt = """
You are an helpful assistant for a simple CLI chat. Only respond with text messages. Get creative with the answers!

If the user indicates they want to stop, quit, exit, end the chat, or say goodbye,
call the end_interaction tool. Do not merely respond with text in that case.
"""

MODEL = "gpt-5-nano"

MODEL_PRICING_PER_1M = {
    "gpt-5-nano": {
        "input": 0.05,
        "cached_input": 0.005,
        "output": 0.40,
    }
}

tools = [
    {
        "type": "function",
        "name": "end_interaction",
        "description": "End the CLI chat session when the user wants to stop, exit, quit, or end the conversation.",
        "parameters": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": "Brief reason the interaction is ending."
                }
            },
            "required": ["reason"],
            "additionalProperties": False
        },
        "strict": True
    }
]

def get_usage_value(obj, field_name, default=0):
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(field_name, default)
    return getattr(obj, field_name, default)


def estimate_total_cost(response, model):
    pricing = MODEL_PRICING_PER_1M[model]
    usage = response.usage

    input_tokens = get_usage_value(usage, "input_tokens")
    output_tokens = get_usage_value(usage, "output_tokens")

    input_details = get_usage_value(usage, "input_tokens_details", {})
    cached_tokens = get_usage_value(input_details, "cached_tokens")

    non_cached_input_tokens = max(input_tokens - cached_tokens, 0)

    input_cost = (non_cached_input_tokens / 1_000_000) * pricing["input"]
    cached_input_cost = (cached_tokens / 1_000_000) * pricing["cached_input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]

    return input_cost + cached_input_cost + output_cost

def end_interaction(reason: str = "User or assistant ended the conversation."):
    return {
        "should_end": True,
        "reason": reason
    }

def process_assistant_tool_calls(response) -> bool:
    """
    Returns True if the interaction should end.
    """
    for item in response.output:
        if item.type != "function_call":
            continue
        print(f"Function call ID: {item.call_id}")
        if item.name == "end_interaction":
            arguments = json.loads(item.arguments or "{}")
            result = end_interaction(**arguments)
            print(f"Ending interaction: {result['reason']}")
            return True
    return False



def main():

    print("Python CLI Chat Client")

    print("Type 'exit', 'quit', or Ctrl+C to stop.\n")

    previous_response_id = None

    while True:
        try:
            user_input = input("Enter a message: ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        if not user_input:
            continue
        try:
            print(f"You: {user_input}\n")
            response = client.responses.create(
                model=MODEL,
                instructions=system_prompt,
                input=user_input,
                previous_response_id=previous_response_id,
                tools=tools
            )
            previous_response_id = response.id

            if response.output_text:
                print(f"\nAssistant: {response.output_text}\n")
            
            should_end_interaction = process_assistant_tool_calls(response)

            print(f"Tokens used: {response.usage.total_tokens:,}")

            cost = estimate_total_cost(response, MODEL)
            print(f"Estimated cost: ${cost:.8f}\n\n")
            if should_end_interaction:
                break

        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()