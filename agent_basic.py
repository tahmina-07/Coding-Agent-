import json
history = []
def mock_llm(prompt, history):
    prompt_lower = prompt.strip().lower()
    if prompt_lower.endswith("?"):
        return "That's a great question! I don't have a real model here, but I can show you how you'd call one."
    if "read file" in prompt_lower:
        return json.dumps({"tool": "read_file", "arguments": {"file_path": "example.txt"}})
    if "run" in prompt_lower:
        return json.dumps({"tool": "run_code", "arguments": {"code": "print('Hello, World!')"}})
    return "I heard: " + prompt

def call_llm_and_parse(prompt, history):
    raw = mock_llm(prompt, history)
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict) and "tool" in parsed and "arguments" in parsed:
            return parsed
    except Exception:
        pass
    return {"type": "text", "payload": raw}

def main_loop():
    print("Welcome to the basic agent. Type 'exit' to quit.")   
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        response = call_llm_and_parse(user_input, history)
        if response.get("type") == "text":
            print("Agent:", response["payload"])
        else:
            tool = response["tool"]
            arguments = response["arguments"]
            print(f"Agent wants to use tool: {tool} with arguments: {arguments}")
        history.append({"user": user_input, "agent": response})
if __name__ == "__main__":
    main_loop()