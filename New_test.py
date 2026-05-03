import os
import traceback
from dotenv import load_dotenv
import google.generativeai as genai

# Load from specific .env path
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path)

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("GEMINI_API_KEY not found!")
        print("Available env vars:", list(os.environ.keys())[:10])
        raise SystemExit("Please set GEMINI_API_KEY in .env file")
    
    print(f"[OK] API Key found: {api_key[:10]}...")
    
    try:
        genai.configure(api_key=api_key)
        
        # List available models
        print("\nAvailable models:")
        models_list = []
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
                models_list.append(model.name)
        
        # Use the latest model
        model_name = "models/gemini-1.5-flash"
        if model_name not in models_list:
            model_name = models_list[0]
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Who is India's PM?")
        print("\n[OK] Success!")
        print(response.text)
    except Exception as e:
        print(f"\n[ERROR] Error: {type(e).__name__}")
        print(f"Message: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()