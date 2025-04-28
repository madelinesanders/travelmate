import ollama

def generate_packing_list(weather_summary, activities):
    prompt = f"""
You are a smart travel assistant. Based on the following weather and activities, suggest a detailed packing list.

Weather Summary:
{weather_summary}

Planned Activities:
{', '.join(activities)}

Please organize your answer clearly with bullet points.
"""
    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
            options={"timeout": 30}  # 30 seconds timeout
        )
        return response['message']['content']
    except Exception as e:
        print(f"❌ Ollama call failed: {e}")
        return "Sorry, something went wrong while generating your packing list."
