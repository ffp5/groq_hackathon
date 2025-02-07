from groq import Groq

def generate_dialogue2(agent_name, other_agent_name, context):
    client = Groq(api_key="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")
    messages = [
        {
            "role": "system",
            "content": ("You are a witty villager with a sassy attitude. "
                       "Reply with ONE SHORT LINE ONLY (max 10 words) that's clever and funny. "
                       "Use comebacks, witty remarks, or quick jokes. "
                       "Examples: 'Oh great, another charmer! *rolls eyes dramatically*' "
                       "or 'Did you practice that line in the mirror?' "
                       "Keep it VERY brief and snappy!")
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
