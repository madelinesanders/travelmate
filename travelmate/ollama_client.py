import ollama

def generate_packing_list(weather_summary, activities):
    prompt = f"""
You are a smart travel assistant. Based on the following weather and activities, suggest a detailed packing list.

Weather Summary:
{weather_summary}

Planned Activities:
{', '.join(activities)}

Please organize your answer clearly with bullet points.
Be concise and practical.
"""

    try:
        print("Sending request to Ollama...")

        client = ollama.Client(host='http://localhost:11434')

        response = client.chat(
            model="mistral",  # Or "tinyllama" if you prefer speed
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0.2
                # No num_predict limit here!
            }
        )

        print("Received response from Ollama!")

        return response['message']['content']
    except Exception as e:
        print(f"Ollama call failed: {e}")
        return "Sorry, something went wrong while generating your packing list."

def generate_travel_tips(summary):
    prompt = f"""
You are a smart travel assistant.

For the following trip destination and dates, please generate a short travel guide that includes:
- Cultural dress expectations (especially important norms, taboos, etc.)
- Must-have items that travelers should pack
- Basic local information (e.g., tipping customs, language spoken, important notes)

Destination Summary:
{summary}

Keep the advice concise, clear, and organized into sections.
"""

    try:
        print("Sending travel tips request to Ollama...")

        client = ollama.Client(host='http://localhost:11434')

        response = client.chat(
            model="mistral",  # Or tinyllama if you prefer speed
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0.3
            }
        )

        print("Received travel tips from Ollama!")

        return response['message']['content']
    except Exception as e:
        print(f"Ollama call failed for travel tips: {e}")
        return "Sorry, something went wrong while generating your travel tips."
