import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
from features import extract_features

app = FastAPI(title="SafePeek Phase-1 API", version="1.0")

# Chrome Extension se requests allow karne ke liye CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "models", "safepeek_rf.pkl")
model = joblib.load(model_path)

class URLRequest(BaseModel):
    url: str

def get_reasons(feats: list) -> list:
    reasons = []
    if feats[0] > 75:
        reasons.append("Unusually long URL (>75 characters)")
    if feats[4] >= 3:
        reasons.append("Multiple hyphens detected in URL")
    if feats[5] > 0:
        reasons.append("Contains '@' redirection symbol")
    if feats[9] == 0:
        reasons.append("Insecure HTTP protocol (No SSL/TLS)")
    if feats[10] == 1:
        reasons.append("Raw IP address used instead of domain name")
    if feats[11] >= 2:
        reasons.append("Multiple suspicious subdomains detected")
    if feats[12] >= 1:
        reasons.append("Sensitive keywords found (login/verify/kyc/banking)")
    if feats[13] == 1:
        reasons.append("URL shortener hides actual destination")
    return reasons if reasons else ["Clean domain structure & HTTPS verified"]

@app.get("/")
def home():
    return {"message": "SafePeek API is running!"}

@app.post("/predict")
def predict_url(req: URLRequest):
    feats = extract_features(req.url)
    prob = float(model.predict_proba([feats])[0][1])

    if prob >= 0.75:
        status = "Phishing"
    elif prob >= 0.40:
        status = "Suspicious"
    else:
        status = "Safe"

    return {
        "url": req.url,
        "status": status,
        "risk_score": round(prob * 100, 2),
        "reasons": get_reasons(feats)
    }