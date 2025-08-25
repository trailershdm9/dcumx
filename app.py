from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 🔑 Replace with your real GDTOT credentials
EMAIL = "YourEmail@gmail.com"
API_TOKEN = "kVTKqsfQlU39uQnqh2Zb4LQwneUNU"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    url = request.form["url"].strip()

    # Decide API endpoint
    if "/folders/" in url:   # Google Drive folder link
        api_url = "https://new.gdtot.com/api/upload/folder"
    else:  # Single file link
        api_url = "https://new.gdtot.com/api/upload/link"

    payload = {
        "email": EMAIL,
        "api_token": API_TOKEN,
        "url": url
    }

    try:
        response = requests.post(api_url, data=payload)
        data = response.json()

        if data.get("status") and "data" in data:
            results = [item["url"] for item in data["data"]]
            return render_template("result.html", results=results)
        else:
            error_msg = data.get("message", "Failed to fetch link.")
            return render_template("result.html", results=[f"❌ Error: {error_msg}"])

    except Exception as e:
        return render_template("result.html", results=[f"⚠️ Exception: {str(e)}"])

if __name__ == "__main__":
    app.run(debug=True)
