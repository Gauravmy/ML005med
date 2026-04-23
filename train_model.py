"""
Machine Learning Model Training Script
This script trains a Logistic Regression model to predict pass/fail based on study hours and attendance
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Sample training data: [Study Hours, Attendance %]
X = np.array([
    [2, 60], [3, 65], [4, 75], [5, 85], [6, 90],
    [1, 50], [2, 55], [3, 70], [4, 80], [5, 88],
    [6, 92], [7, 95], [1, 45], [2, 52], [3, 68],
    [4, 78], [5, 87], [6, 91], [7, 96], [8, 98],
    [1, 40], [2, 48], [3, 62], [4, 72], [5, 82]
])

# Labels: 0 = Fail, 1 = Pass
# Students with low study hours and attendance fail; high values = pass
y = np.array([0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features (important for logistic regression)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the Logistic Regression model
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate model
accuracy = model.score(X_test_scaled, y_test)
print(f"Model Accuracy: {accuracy:.2%}")
print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

# Save the model and scaler using joblib
joblib.dump(model, 'models/model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')

print("✓ Model saved as 'models/model.pkl'")
print("✓ Scaler saved as 'models/scaler.pkl'")
print("\nModel is ready for predictions!")
