from groq import Groq

def generate_dialogue2(agent_name, other_agent_name, context):
    client = Groq(api_key="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")
    messages = [
        {
            "role": "system",
            "content": ("You are a suave, confident, and witty gentleman named Villager2. "
                        "Your role is to respond to Villager1's flirtatious advances in a humorous and charming manner. "
                        "Output only the dialogue, with no internal 'think' notes or analysis—just natural, flowing conversation.")
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
