# app.py
import os
import streamlit as st
from PIL import Image
import io
from openai import OpenAI

# -----------------------------
# Read API key from environment
# -----------------------------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Missing OPENAI_API_KEY. Set it before running the app.")
client = OpenAI(api_key=api_key)

# -----------------------------
# Vibes dictionary
# -----------------------------
vibe_prompts = {
    "Funny 😄": "Make it funny, playful, use casual language and emojis.",
    "Aesthetic ✨": "Stylish, aesthetic, visually appealing captions.",
    "Professional 💼": "Professional tone, polished, concise.",
    "Emotional ❤️": "Emotional, heartfelt, expressive.",
    "Confident 🔥": "Confident, bold, energetic.",
    "Casual 🧢": "Relaxed, friendly, everyday tone.",
    "Minimal 🧘": "Short, minimal, simple wording."
}

# -----------------------------
# Image-to-text summarization
# -----------------------------
def summarize_image(image_file):
    """Generate a short text description of the uploaded image."""
    # Convert image to bytes
    img_bytes = image_file.read()
    # Optional: could save to temp file if needed
    prompt = (
        "You are an AI that summarizes the content of images in 1-2 sentences. "
        "Describe only what is visible in the image, do not guess intent or emotion."
    )
    # Use GPT with image bytes encoded as string (placeholder for simple demo)
    # For real image understanding, could integrate BLIP or other model
    description = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Image bytes (length {len(img_bytes)}): {img_bytes[:50]}..."}
        ]
    )
    return description.choices[0].message.content

# -----------------------------
# Caption generation
# -----------------------------
def generate_captions(image_summary, vibe, n=5):
    prompt = (
        f"Generate {n} social media captions for the following image description:\n"
        f"{image_summary}\n"
        f"Style instructions based on vibe: {vibe_prompts[vibe]}\n"
        f"Provide captions as a numbered list."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a social media caption generator."},
            {"role": "user", "content": prompt}
        ]
    )
    captions_text = response.choices[0].message.content
    # Split numbered list into separate captions
    lines = [line.strip() for line in captions_text.split("\n") if line.strip()]
    return lines

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Image-Aware Caption Generator with Vibe Control")

uploaded_image = st.file_uploader("Upload your photo", type=["jpg", "png"])
selected_vibe = st.selectbox("Choose a vibe", list(vibe_prompts.keys()))

if uploaded_image:
    with st.spinner("Analyzing image and generating captions..."):
        try:
            image_summary = summarize_image(uploaded_image)
            captions = generate_captions(image_summary, selected_vibe)
            
            st.subheader("Generated Captions:")
            for i, caption in enumerate(captions):
                st.write(f"{i+1}. {caption}")
            
            if st.button("Regenerate"):
                captions = generate_captions(image_summary, selected_vibe)
                for i, caption in enumerate(captions):
                    st.write(f"{i+1}. {caption}")
        except Exception as e:
            st.error(f"Error generating captions: {e}")
