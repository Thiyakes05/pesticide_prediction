# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import MinMaxScaler, LabelEncoder
# from sklearn.model_selection import train_test_split
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense

# # Load dataset
# data = pd.read_csv(r'C:\Users\venis\Desktop\wise-aithon\cropdata.csv')
# data.columns = data.columns.str.strip()

# # Encode categorical variables
# encoder_pest = LabelEncoder()
# data['Pest/Disease'] = encoder_pest.fit_transform(data['Pest/Disease'])

# encoder_location = LabelEncoder()
# data['Location'] = encoder_location.fit_transform(data['Location'])

# # Prepare features and target for temperature prediction
# features = data[['Observation Year', 'Standard Week', 'RH1(%)', 'RH2(%)', 'RF(mm)', 'WS(kmph)', 'SSH(hrs)', 'EVP(mm)', 'Location']]
# target = data[['MaxT(°C)', 'MinT(°C)']]

# # Scaling features and target
# scaler_features = MinMaxScaler()
# features_scaled = scaler_features.fit_transform(features)

# scaler_targets = MinMaxScaler()
# target_scaled = scaler_targets.fit_transform(target)

# # Function to create sequences for LSTM
# def create_sequences(X, y, time_steps=10):
#     Xs, ys = [], []
#     for i in range(len(X) - time_steps):
#         Xs.append(X[i:i + time_steps])
#         ys.append(y[i + time_steps])
#     return np.array(Xs), np.array(ys)

# time_steps = 10
# X, y = create_sequences(features_scaled, target_scaled, time_steps)

# # Split the data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Build the temperature prediction model
# model = Sequential()
# model.add(LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True))
# model.add(LSTM(64, return_sequences=False))
# model.add(Dense(25, activation='relu'))
# model.add(Dense(2))  # Predicting MaxT and MinT

# model.compile(optimizer='adam', loss='mean_squared_error')

# # Train the temperature prediction model
# # history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

# # Predict and rescale the temperature for test data
# y_pred = model.predict(X_test)
# y_pred_rescaled = scaler_targets.inverse_transform(y_pred)
# y_test_rescaled = scaler_targets.inverse_transform(y_test)

# # Prepare the dataset for pest/disease prediction using predicted temperatures
# data_predicted = data.copy()
# data_predicted['Pred_MaxT'] = np.nan
# data_predicted['Pred_MinT'] = np.nan

# # Insert predicted temperatures into the dataset
# data_predicted.iloc[-len(y_pred_rescaled):, data_predicted.columns.get_loc('Pred_MaxT')] = y_pred_rescaled[:, 0]
# data_predicted.iloc[-len(y_pred_rescaled):, data_predicted.columns.get_loc('Pred_MinT')] = y_pred_rescaled[:, 1]

# # Prepare features and target for pest/disease prediction
# features_pest = data_predicted[['Observation Year', 'Standard Week', 'Pred_MaxT', 'Pred_MinT', 'RH1(%)', 'RH2(%)', 'RF(mm)', 'WS(kmph)', 'SSH(hrs)', 'EVP(mm)', 'Location']]
# target_pest = data_predicted['Pest/Disease']

# # Scale pest prediction features
# features_pest_scaled = scaler_features.fit_transform(features_pest)

# # Create sequences for pest/disease prediction
# X_pest, y_pest = create_sequences(features_pest_scaled, target_pest.values, time_steps)

# # Split the data for pest/disease prediction
# X_pest_train, X_pest_test, y_pest_train, y_pest_test = train_test_split(X_pest, y_pest, test_size=0.2, random_state=42)

# # Build the pest/disease prediction model
# model_pest = Sequential()
# model_pest.add(LSTM(64, input_shape=(X_pest_train.shape[1], X_pest_train.shape[2]), return_sequences=True))
# model_pest.add(LSTM(64, return_sequences=False))
# model_pest.add(Dense(25, activation='relu'))
# model_pest.add(Dense(1))  # Predicting Pest/Disease

# model_pest.compile(optimizer='adam', loss='mean_squared_error')

# # Train the pest/disease prediction model
# # history_pest = model_pest.fit(X_pest_train, y_pest_train, epochs=20, batch_size=32, validation_data=(X_pest_test, y_pest_test))

# # Function to predict temperature and pest/disease based on location input
# def predict_based_on_location(location):
#     # Encode the input location
#     location_encoded = encoder_location.transform([location])[0]

#     # Create a sample feature array for the temperature prediction (MaxT, MinT)
#     sample_features = np.mean(features_scaled, axis=0)  # Use mean values for all other features
#     sample_features[-1] = location_encoded  # Set the location to the user's input
    
#     # Prepare the sequence input for temperature prediction
#     sequence_input_temp = np.tile(sample_features, (time_steps, 1))  # Tile the same feature for sequence
#     sequence_input_temp = np.expand_dims(sequence_input_temp, axis=0)  # Reshape to match input shape for the model

#     # Predict MaxT and MinT
#     temp_pred_scaled = model.predict(sequence_input_temp)[0]  # Get predicted values for MaxT and MinT
#     temp_pred_rescaled = scaler_targets.inverse_transform([temp_pred_scaled])[0]  # Rescale to original values

#     predicted_maxt = temp_pred_rescaled[0]
#     predicted_mint = temp_pred_rescaled[1]

#     print(f"Predicted MaxT for {location}: {predicted_maxt}")
#     print(f"Predicted MinT for {location}: {predicted_mint}")

#     # Now use the predicted temperature to predict pest/disease
#     sample_features_pest = np.append(sample_features, [predicted_maxt, predicted_mint])  # Add predicted MaxT and MinT
#     sequence_input_pest = np.tile(sample_features_pest, (time_steps, 1))  # Prepare the sequence for pest prediction
#     sequence_input_pest = np.expand_dims(sequence_input_pest, axis=0)

#     # Predict pest/disease
#     pest_pred_scaled = model_pest.predict(sequence_input_pest)[0]
#     pest_pred_rounded = np.round(pest_pred_scaled).astype(int)
#     pest_pred_label = encoder_pest.inverse_transform(pest_pred_rounded.flatten())[0]  # Convert back to label

#     print(f"Predicted Pest/Disease for {location}: {pest_pred_label}")
#     return predicted_maxt, predicted_mint, pest_pred_label



# # Example usage
# location_input = input("Enter location: ")
# predict_based_on_location(location_input)
