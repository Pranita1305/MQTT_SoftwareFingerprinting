import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("captures/dataset.csv")

# Encode categorical features
le_topic = LabelEncoder()
le_payload = LabelEncoder()
le_device = LabelEncoder()
le_version = LabelEncoder()
le_broker = LabelEncoder()

df["topic_enc"] = le_topic.fit_transform(df["topic"])
df["payload_enc"] = le_payload.fit_transform(df["payload_type"])
df["device_enc"] = le_device.fit_transform(df["device"])
df["version_enc"] = le_version.fit_transform(df["device_version"])
df["broker_enc"] = le_broker.fit_transform(df["broker"])

X = df[["topic_enc", "qos", "payload_enc", "payload_len", "msg_type"]]
y = df[["device_enc", "version_enc", "broker_enc"]]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Multi-output model
model = MultiOutputClassifier(RandomForestClassifier(random_state=42))
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

print("\nDevice Report:\n")
print(
    classification_report(
        y_test["device_enc"],
        y_pred[:, 0],
        labels=list(range(len(le_device.classes_))),
        target_names=le_device.classes_,
        zero_division=0,
    )
)

print("\n Version Report:\n")
print(
    classification_report(
        y_test["version_enc"],
        y_pred[:, 1],
        labels=list(range(len(le_version.classes_))),
        target_names=le_version.classes_,
        zero_division=0,
    )
)

print("\n Broker Report:\n")
print(
    classification_report(
        y_test["broker_enc"],
        y_pred[:, 2],
        labels=list(range(len(le_broker.classes_))),
        target_names=le_broker.classes_,
        zero_division=0,
    )
)


