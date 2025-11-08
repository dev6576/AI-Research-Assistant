import os
import requests
from pathlib import Path
import hashlib

def download_model():
    """Download the quantized Llama-2 model for local usage."""
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Model details
    model_name = "llama-2-7b-chat.Q4_K_M.gguf"
    model_path = models_dir / model_name
    
    # Check if model already exists
    if model_path.exists():
        print(f"Model already exists at {model_path}")
        return
    
    # Model URL (replace with actual hosted model URL)
    model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
    
    print(f"Downloading {model_name}...")
    print("This might take a while depending on your internet connection.")
    
    # Download with progress
    response = requests.get(model_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(model_path, 'wb') as f:
        if total_size == 0:
            f.write(response.content)
        else:
            downloaded = 0
            for data in response.iter_content(chunk_size=4096):
                downloaded += len(data)
                f.write(data)
                done = int(50 * downloaded / total_size)
                print(f"\rDownloading: [{'=' * done}{' ' * (50-done)}] {downloaded}/{total_size} bytes", end='')
    
    print("\nDownload complete!")

if __name__ == "__main__":
    download_model()