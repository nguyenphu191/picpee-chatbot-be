import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LLM_API_KEY")
model_name = os.getenv("EMBEDDING_MODEL_NAME")

print(f"Testing with Model: {model_name}")
print(f"API Key start: {api_key[:10]}...")

genai.configure(api_key=api_key)

try:
    print("\n--- Listing Models ---")
    for m in genai.list_models():
        if 'embedContent' in m.supported_generation_methods:
            print(f"Model ID: {m.name}")
    
    print("\n--- Testing Embedding ---")
    # Ensure model name has models/ prefix if needed
    full_model_name = model_name if model_name.startswith("models/") else f"models/{model_name}"
    
    result = genai.embed_content(
        model=full_model_name,
        content="Hello world",
        task_type="retrieval_query"
    )
    print("✅ Success!")
    print(f"Vector size: {len(result['embedding'])}")

except Exception as e:
    print(f"❌ Failed: {str(e)}")
