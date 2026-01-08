"""
Image-Aware Caption Generator with Vibe Control
Single-file deployable mini-app (Option 1 - simple)

Usage:
1. Set your OpenAI API key in terminal (temporary session):
   - Mac/Linux: export OPENAI_API_KEY="sk-xxxx"
   - Windows PowerShell: $env:OPENAI_API_KEY="sk-xxxx"
2. Run the app:
   python app.py
"""

# ----------------------------
# Step 0: Imports & setup
# ----------------------------
import os
import streamlit as st
from openai import OpenAI

# Read API key from environment variable (secure)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Missing OPENAI_API_KEY. Set it before running the app.")
client = OpenAI(api_key=api_key)

# ----------------------------
# Step 1: Vibe prompts
# ----------------------------
vibe_prompts = {
    "Funny": "witty, playful, light humor",
    "Aesthetic": "soft, artistic, visually descriptive",
    "Casual": "relaxed, friendly, everyday language",
    "Confident": "bold, self-assured, strong statements",
    "Emotional": "thoughtful, reflective, heartfelt",
    "Minimal": "concise, simple, minimalistic"
}

# ----------------------------
# Step 2: Build AI prompt
# ----------------------------
def build_prompt(image_description, vibe):
    prompt = f"""
You are a professional social media caption writer.

Image description:
{image_description}

Generate 5 captions that match:
- Vibe: {vibe} ({vibe_prompts[vibe]})

Avoid generic phrases. Each caption should feel natural, human, and engaging.
"""
    return prompt

# ----------------------------
# Step 3: Streamlit UI
# ----------------------------
st.title("Image-Aware Caption Generator (Simple Version)")

uploaded_image = st.file_uploader("Upload your photo", type=["jpg","png"])
selected_vibe = st.selectbox("Choose a vibe", list(vibe_prompts.keys()))

# ----------------------------
# Step 4: Generate captions
# ----------------------------
def generate_captions(image_file, vibe):
    """
    Generates 5 captions for a given image and vibe.
    """
    # Placeholder image description for demo
    image_description = "A person standing outdoors during golden hour"
    prompt = build_prompt(image_description, vibe)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            input=image_file
        )
        captions_text = response.choices[0].message.content
        captions = [line.strip() for line in captions_text.split("\n") if line.strip()]
        return captions[:5]
    except Exception as e:
        return [f"Error generating captions: {str(e)}"]

# ----------------------------
# Step 5: Button logic & display
# ----------------------------
if uploaded_image and st.button("Generate Captions"):
    captions = generate_captions(uploaded_image, selected_vibe)
    st.subheader("Captions")
    for i, c in enumerate(captions):
        st.write(f"{i+1}. {c}")

if uploaded_image and st.button("Regenerate"):
    captions = generate_captions(uploaded_image, selected_vibe)
    st.subheader("Captions (Regenerated)")
    for i, c in enumerate(captions):
        st.write(f"{i+1}. {c}")
