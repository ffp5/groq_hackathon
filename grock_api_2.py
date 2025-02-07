from groq import Groq

def generate_dialogue2(agent_name, other_agent_name, context):
    client = Groq(api_key="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")
    messages = [
        {
            "role": "system",
            "content": ("IMPORTANT: Output ONLY one flirty line, no thinking! "
                       "You are a charming lover with a playful attitude. "
                       "Mix romance with gentle teasing. "
                       "Examples: "
                       "'Can't take your eyes off me, can you? 😏' "
                       "'Your sass is showing, darling... I like it!' "
                       "'Still using those cheesy lines? They're working...'")
        },
        {
            "role": "user",
            "content": "Respond to your lover's flirting with sass"
        }
    ]
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=messages,
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=True,
        stop=None,
    )
    dialogue = ""
    for chunk in completion:
        dialogue += (chunk.choices[0].delta.content or "")
    return dialogue
