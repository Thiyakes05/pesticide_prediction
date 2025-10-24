# import streamlit as st
# import requests
# import json

# # Streamlit app title
# st.title('Crop Pest Prediction')

# # Location input
# location = st.text_input('Enter location: ', ' ')

# # Submit button
# if st.button('Predict'):
#     if location:
#         response = requests.post('http://127.0.0.1:8000/home/predict/', data={'location': location})
#         if response.status_code == 200:
#             data = response.json()
#             st.write(f"Predicted Max Temperature: {data['Pred_MaxT']}")
#             st.write(f"Predicted Min Temperature: {data['Pred_MinT']}")
#             st.write(f"Pest/Disease Prediction: {data['pest_pred_label'
#             ]}")
#         else:
#             st.write("Error in prediction.")
#     else:
#         st.write("Please enter a location.")




