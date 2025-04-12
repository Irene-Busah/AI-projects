import numpy as np
import joblib
from sklearn.linear_model import LinearRegression

# creating dummy data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# training the model
model = LinearRegression()
model.fit(X, y)

# saving the model
joblib.dump(model, 'model.pkl')
print("Model Saved!")
