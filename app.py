import openai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generateimage/<prompt>')
def generate(prompt):
    try:
        print("Prompt:", prompt)
        response = openai.Image.create(prompt=prompt, n=4, size="256x256")  # Generate 4 images
        
        # Extract URLs from response
        image_urls = [img["url"] for img in response["data"]]
        
        return jsonify({"image_urls": image_urls})
    
    except openai.error.RateLimitError as e:
        return jsonify({"error": "Rate limit exceeded. Try again later!"}), 429
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)
