from groq import Groq

def generate_dialogue1(agent_name, other_agent_name, context):
    client = Groq(api_key="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")
    messages = [
        {
            "role": "system",
            "content": ("IMPORTANT: Output ONLY one flirty line, no thinking! "
                       "You are a playfully sassy lover. Be romantic but teasing. "
                       "Examples: "
                       "'Miss me already, handsome?' "
                       "'Caught you staring... again! 😘' "
                       "'Your pickup lines are still terrible, but I love you anyway!'")
        },
        {
            "role": "user",
            "content": "Say something flirty and sassy to your lover"
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
