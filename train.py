from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from app.features import FEATURES, build_features

df = pd.read_csv("data/financial_risk_demo.csv")
X = build_features(df)[FEATURES]
y = df["risk_label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

base = RandomForestClassifier(
    n_estimators=350,
    max_depth=8,
    min_samples_leaf=5,
    class_weight="balanced",
    random_state=42,
)
model = CalibratedClassifierCV(base, method="sigmoid", cv=3)
model.fit(X_train, y_train)

pred = model.predict_proba(X_test)[:, 1]
print("ROC-AUC:", round(roc_auc_score(y_test, pred), 4))
print(classification_report(y_test, (pred >= 0.5).astype(int)))

Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/risk_model.joblib")
Path("models/features.json").write_text(json.dumps(FEATURES, indent=2))
print("Saved models/risk_model.joblib")
