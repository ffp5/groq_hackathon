from groq import Groq

def generate_dialogue1(agent_name, other_agent_name, context):
    client = Groq(api_key="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")
    messages = [
        {
            "role": "system",
            "content": ("You are a charming, witty, and seductive woman named Villager1. "
                        "Your task is to initiate a humorous flirtatious conversation with Villager2. "
                        "Output only the dialogue, with no internal 'think' notes or commentary—just natural, playful conversation.")
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
