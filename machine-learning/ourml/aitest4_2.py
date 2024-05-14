import pandas as pd
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

# Load data from CSV file
new_data = pd.read_csv('data_test_small.csv')

# Slice the DataFrame to include only the features (first 12 columns)
new_data_features = new_data.iloc[:, 1:13]
print(new_data_features)

# Scale the features
scaler = StandardScaler()
new_data_scaled = scaler.fit_transform(new_data_features)

# Load the model from file
model = tf.keras.models.load_model('my_model.keras')

# Get the true target values from the 13th column
new_data = pd.read_csv('target_test_small.csv')
true_values = new_data.iloc[:, 1]
print(true_values)

# Make predictions on the new data
predictions = model.predict(new_data_scaled)
print(predictions)

predictions_df = pd.DataFrame(predictions, columns=['Predictions'])

# Save the predictions to a new CSV file
#predictions_df.to_csv('predictions.csv', index=False)
# Calculate the mean squared error (MSE)
mae = mean_absolute_error(true_values, predictions)

print("MAE:", mae)
