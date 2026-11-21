import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from features import extract_features

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "data", "urldata.csv")
models_dir = os.path.join(base_dir, "models")
os.makedirs(models_dir, exist_ok=True)

# 1. Load Dataset
print("Loading dataset...")
df = pd.read_csv(csv_path).dropna()

print("Extracting 15 lexical & structural features from 10,000 URLs...")
X = [extract_features(u) for u in df["url"]]
y = df["label"].values

# 2. Train-Test Split (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Train Random Forest Classifier
print("Training Random Forest model...")
model = RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# 4. Evaluate Performance
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred) * 100
print(f"\nModel Accuracy: {acc:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Safe", "Phishing"]))

# 5. Save Confusion Matrix Image (Project Report Chapter 6 ke liye)
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 4))
sns.heatmap(
    cm, annot=True, fmt="d", cmap="Blues",
    xticklabels=["Safe", "Phishing"],
    yticklabels=["Safe", "Phishing"]
)
plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.title(f"SafePeek Confusion Matrix (Accuracy: {acc:.2f}%)")
cm_path = os.path.join(models_dir, "confusion_matrix.png")
plt.savefig(cm_path, dpi=300, bbox_inches="tight")

# 6. Save Trained Model (.pkl)
model_path = os.path.join(models_dir, "safepeek_rf.pkl")
joblib.dump(model, model_path)
print(f"Saved model to: {model_path}")
print(f"Saved Confusion Matrix image to: {cm_path}")