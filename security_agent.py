import json
from openai import OpenAI
from rag import load_chunks, search
from summary import summary

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
chunks = load_chunks("standards")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_summary",
            "description": "Get the current scan results: code findings by severity and vulnerable dependencies. Use for any question about current findings.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_standards",
            "description": "Search the company security standards. Use for questions about policy or fix deadlines.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
]

def run_tool(name, args):
    if name == "get_summary":
        return json.dumps(summary())
    if name == "search_standards":
        hits = search(args.get("query", ""), chunks)
        return "\n\n".join(f"[{c['source']}] {c['text']}" for c in hits) or "No matching standards found."
    return "Unknown tool."

messages = [{
    "role": "system",
    "content": (
        "You are a security assistant. Use the tools to get facts before answering. "
        "Answer only from tool results, cite the source file for policy claims, "
        "and say 'not found' if the tools return nothing useful."
    ),
}]

question = input("Ask a question: ")
messages.append({"role": "user", "content": question})

for _ in range(5):
    resp = client.chat.completions.create(model="qwen2.5:7b", messages=messages, tools=tools)
    msg = resp.choices[0].message
    messages.append(msg.model_dump(exclude_none=True))
    if not msg.tool_calls:
        break
    for call in msg.tool_calls:
        args = json.loads(call.function.arguments or "{}")
        print("TOOL CALL:", call.function.name, args)
        messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": run_tool(call.function.name, args),
        })

print(msg.content)
