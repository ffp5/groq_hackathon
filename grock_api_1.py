from groq import Groq

def generate_dialogue1(agent_name, other_agent_name, context):
    client = Groq(api_key="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")
    messages = [
        {
            "role": "system",
            "content": ("You are a flirty villager with a funny personality. "
                       "Generate ONE SHORT LINE ONLY (max 10 words) that's playful and funny. "
                       "Use puns, silly pickup lines, or quick jokes. "
                       "Examples: 'Is your name WiFi? Because I'm feeling a connection!' "
                       "or 'You must be a magician... I'm under your spell!' "
                       "Keep it VERY brief and punchy!")
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
