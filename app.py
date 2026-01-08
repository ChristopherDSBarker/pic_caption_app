# app.py
import os
import streamlit as st
from openai import OpenAI

# --- Read API key from environment variable ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Missing OPENAI_API_KEY. Set it before running the app.")
client = OpenAI(api_key=api_key)

# --- Vibe prompts (embedded, no separate file) ---
vibe_prompts = {
    "Funny 😄": "Use humor, playful words, short sentences, and emojis.",
    "Aesthetic ✨": "Use elegant words, focus on visuals, include soft emojis if appropriate.",
    "Professional 💼": "Use formal tone, clear language, no emojis, concise sentences.",
    "Emotional ❤️": "Use heartfelt, expressive language, include emotional words and emojis.",
    "Confident 🔥": "Use assertive, bold language, exclamation marks, and confident emojis.",
    "Casual 🧢": "Use informal, relaxed language, conversational style, light emojis.",
    "Minimal 🧘": "Use very short sentences or phrases, minimal words, few or no emojis."
}

# --- Build prompt using image description + vibe ---
def build_prompt(image_description, vibe):
    vibe_text = vibe_prompts.get(vibe, "")
    prompt = (
        f"Generate 5 captions for the following image description, matching the vibe '{vibe}':\n\n"
        f"{image_description}\n\n"
        f"Use the following style:\n{vibe_text}"
    )
    return prompt

# --- Generate captions ---
def generate_captions(image_file, selected_vibe):
    # Placeholder description for simple demo
    image_description = "A person standing outdoors during golden hour"
    
    prompt = build_prompt(image_description, selected_vibe)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        captions_text = response.choices[0].message.content
        captions = [line.strip() for line in captions_text.split("\n") if line.strip()]
        return captions[:5]
    except Exception as e:
        return [f"Error generating captions: {str(e)}"]

# --- Streamlit UI ---
st.title("Image-Aware Caption Generator")

uploaded_image = st.file_uploader("Upload your photo", type=["jpg","png"])
selected_vibe = st.selectbox("Choose a vibe", list(vibe_prompts.keys()))

if uploaded_image:
    captions = generate_captions(uploaded_image, selected_vibe)
    for i, caption in enumerate(captions):
        st.write(f"{i+1}. {caption}")

    if st.button("Regenerate"):
        captions = generate_captions(uploaded_image, selected_vibe)
        for i, caption in enumerate(captions):
            st.write(f"{i+1}. {caption}")
