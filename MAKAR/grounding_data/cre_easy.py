import json
import pandas as pd
from datasets import Dataset
import os

# Load the JSON data from the uploaded file
with open("sampled_easy_3k.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def process_entry(entry):
    """
    Process a single entry from the JSON data.
    Extracts the user message as the problem, the assistant message as the answer,
    and uses the provided image paths.
    """
    # Extract user and assistant messages
    user_msg = next((msg for msg in entry["messages"] if msg["role"] == "user"), None)
    assistant_msg = next((msg for msg in entry["messages"] if msg["role"] == "assistant"), None)

    if not user_msg or not assistant_msg:
        raise ValueError("Missing user or assistant message in the entry.")

    user_content = user_msg["content"]
    assistant_content = assistant_msg["content"]

    # Use the provided image paths directly
    image_paths = entry["images"]

    # Read images as bytes
    images_bytes = []
    for img_path in image_paths:
        try:
            with open(img_path, "rb") as img_file:
                images_bytes.append(img_file.read())
        except Exception as e:
            print(f"Error reading image {img_path}: {e}")
            images_bytes.append(None)

    return {
        "problem": user_content,
        "answer": assistant_content,
        "images": images_bytes
    }


# Process all entries
processed_data = [process_entry(entry) for entry in data]

# print("processed_data:",processed_data[0])
# print("processed_data:",processed_data[-1])

# Convert to Hugging Face Dataset
dataset = Dataset.from_list(processed_data)

# Save as Parquet
# dataset.to_parquet("GMNER.parquet")
dataset.to_parquet("new_easy_3k.parquet")