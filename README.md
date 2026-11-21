# 🛡️ SafePeek — Zero-Execution Phishing URL Detector

**SafePeek** is a lightweight, privacy-first cybersecurity browser extension and REST API backend designed to detect phishing and malicious URLs in real time **without loading or executing the target webpage**.

---

## 🚀 Key Features
- **Zero-Execution Architecture:** Analyzes URLs purely through static lexical patterns, ensuring zero risk of drive-by malware downloads or IP/cookie tracking.
- **Ultra-Fast Inference (< 5ms):** Powered by a trained Random Forest classifier served via FastAPI.
- **3-Tier Risk Classification:** Categorizes links into **Safe (`< 40%`)**, **Suspicious (`40% – 70%`)**, and **Phishing (`> 70%`)** with explainable feature flags.
- **Browser Extension UI:** Lightweight popup interface to inspect any URL before clicking or visiting.

---

## 🛠️ Tech Stack
- **Machine Learning:** Python, Scikit-Learn (`RandomForestClassifier`), Pandas, NumPy, Joblib
- **Backend API:** FastAPI, Uvicorn, Pydantic
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Chrome/Edge Manifest V3 Extension)

---

## 🧠 How It Works (15 Lexical Features)
Instead of opening the webpage, `features.py` extracts 15 structural and lexical signals directly from the URL string:
1. Full URL length & Hostname length
2. Presence of raw IPv4 address instead of domain name
3. Presence of `@` symbol (credential redirection trick)
4. Count of dots (`.`), hyphens (`-`), slashes (`/`), and subdomains
5. HTTPS protocol usage (`http` vs `https`)
6. Presence of URL shortening services (`bit.ly`, `tinyurl`, etc.)
7. Suspicious phishing keywords (`login`, `verify`, `update`, `kyc`, `secure`, `banking`, etc.)
8. Digit-to-character ratio and special character count

---

## 📂 Project Structure
```text
SafePeek/
├── app.py               # FastAPI server exposing the /predict endpoint
├── features.py          # 15 lexical feature extraction logic
├── train_model.py       # Dataset splitting, Random Forest training & evaluation
├── prepare_data.py      # Balanced dataset preparation script
├── safepeek_rf.pkl      # Serialized trained Random Forest model (~99% accuracy)
├── urls_dataset.csv     # Balanced training & testing dataset (10,000 URLs)
└── extension/           # Browser extension UI files (manifest.json, popup.html, popup.js)
