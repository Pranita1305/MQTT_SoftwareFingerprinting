import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load dataset
df = pd.read_csv('../captures/dataset.csv')

# Encode categorical features
le_topic = LabelEncoder()
le_payload = LabelEncoder()
le_device = LabelEncoder()

df['topic_enc'] = le_topic.fit_transform(df['topic'])
df['payload_enc'] = le_payload.fit_transform(df['payload_type'])
df['device_enc'] = le_device.fit_transform(df['device'])

X = df[['topic_enc', 'qos', 'payload_enc']]
y = df['device_enc']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred, target_names=le_device.classes_))