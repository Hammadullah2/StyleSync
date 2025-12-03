import os
import json
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from tqdm import tqdm

# ====== CONFIG ======
USE_KAGGLE_PATH = "/kaggle/input/fashion-product-images/styles.csv"
JSON_FOLDER = "/kaggle/input/fashion-product-images/styles/"
TARGET = "masterCategory"

# MLflow tracking server (ngrok URL)
MLFLOW_TRACKING_URI = "https://YOUR_NGROK_URL.ngrok-free.app"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("StyleSync-Training")

# ====== STEP 1 — Load dataset ======
print("Loading styles.csv ...")
df = pd.read_csv(USE_KAGGLE_PATH)

print("Filtering entries with available JSON files...")
json_texts = []
labels = []

for i, row in tqdm(df.iterrows(), total=len(df)):
    json_path = f"{JSON_FOLDER}/{row['id']}.json"
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
            description = data["data"]["productDisplayName"]
            json_texts.append(description)
            labels.append(row[TARGET])
        except Exception as e:
            print(f"Skipping row due to error: {e}")
            continue

text_df = pd.DataFrame({"text": json_texts, "label": labels})

# ====== STEP 2 — Preprocess ======
X_train, X_test, y_train, y_test = train_test_split(
    text_df["text"], text_df["label"], test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(max_features=10000)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ====== STEP 3 — Train ======
clf = LogisticRegression(max_iter=300)

with mlflow.start_run() as run:

    mlflow.log_param("model", "LogisticRegression")
    mlflow.log_param("vectorizer", "TFIDF-10k")

    clf.fit(X_train_vec, y_train)

    preds = clf.predict(X_test_vec)
    acc = accuracy_score(y_test, preds)

    mlflow.log_metric("accuracy", acc)

    mlflow.sklearn.log_model(clf, "model")

    mlflow.log_artifact("styles.csv")

    print(classification_report(y_test, preds))

print("Training done.")
