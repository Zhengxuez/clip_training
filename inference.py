from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

model = CLIPModel.from_pretrained("clip_finetuned").to(device)
processor = CLIPProcessor.from_pretrained("clip_finetuned")


image = Image.open("dataset/chemspeed_clear/image_1.jpg").convert("RGB")

texts = ["chemspeed clear", "chemspeed hazard"]  # Replace with your classes or labels

# Preprocess both image and text
inputs = processor(text=texts, images=image, return_tensors="pt", padding=True).to(device)

# Forward pass
with torch.no_grad():
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # shape: (1, len(texts))
    probs = logits_per_image.softmax(dim=1)      # convert to probabilities

for label, prob in zip(texts, probs[0]):
    print(f"'{label}': {prob.item():.4f}")
