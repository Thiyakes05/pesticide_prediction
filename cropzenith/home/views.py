# # views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from pymongo import MongoClient
from django.utils import timezone
from home.db_con import con_db
# import os
# 
# from home.time_4 import predict_based_on_location
# from tensorflow.keras.models import load_model


# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['farmer']  # Use your actual database name
collection = db['farmer_data']  # Use your actual collection name


# Login view
from django.shortcuts import render, redirect
from pymongo import MongoClient

def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        language = request.POST.get('language')

        if phone_number:
            # Connect to MongoDB
            client = MongoClient('mongodb://localhost:27017/')  # Adjust if using remote or Atlas
            db = client['farmer']  # Database name
            collection = db['farmer_data']  # Collection name

            # Check if user already exists
            existing_user = collection.find_one({"phone_number": phone_number})

            if existing_user:
                # Update language if already exists
                collection.update_one(
                    {"phone_number": phone_number},
                    {"$set": {"language": language}}
                )
            else:
                # Insert new user record
                collection.insert_one({
                    "phone_number": phone_number,
                    "language": language
                })

            # Redirect to homepage with phone number
            return redirect(f'/home/?phone_number={phone_number}')

    return render(request, 'login.html')



# Homepage view
def homepage_view(request):
    phone_number = request.GET.get('phone_number', '')
    return render(request, 'main.html', {'phone_number': phone_number})


# Profile view
def profile_view(request):
    phone_number = request.GET.get('phone_number', '')

    # Find the user's profile by phone number
    profile = collection.find_one({'phone_number': phone_number}) or {}

    return render(request, 'viewprofile.html', {'profile': profile, 'phone_number': phone_number})


# Profile edit view


# Crop information view
def crop_information_view(request):
    phone_number = request.GET.get('phone_number', '')

    if request.method == 'POST':
        crop_name = request.POST.get('crop_name')
        location = request.POST.get('location')
        date = request.POST.get('date')

        # Update the crop information in the same document based on phone number
        collection.update_one(
            {'phone_number': phone_number},
            {'$push': {
                'crop_details': {
                    'crop_name': crop_name,
                    'location': location,
                    'date': date,
                    'submitted_at': timezone.now()
                }
            }},
            upsert=True
        )

        # Redirect to a success page or another page
        return redirect(f'/home/success/?phone_number={phone_number}')

    return render(request, 'crop_details.html', {'phone_number': phone_number})


# Prediction view for temperature and pest
# def predict_view(request):
#     if request.method == 'POST':
#         location = request.POST.get('location')  # Get location from the form

#         # Pass the location to the AI model function and get predictions
#         predicted_maxt, predicted_mint, pest_pred_label = predict_based_on_location(location)

#         # Prepare the response data
#         response_data = {
#             'location': location,
#             'predicted_maxt': predicted_maxt,
#             'predicted_mint': predicted_mint,
#             'pest_prediction': pest_pred_label,
#         }

#         return JsonResponse(response_data)  # Return the result as JSON
#     return JsonResponse({'error': 'Invalid request method'}, status=400)


# from django.shortcuts import render, redirect
# from pymongo import MongoClient
# from django.utils import timezone
# from home.db_con import con_db
# import os
# from home.time_4 import predict_based_on_location


# from tensorflow.keras.models import load_model
# # from home.time_4 import predict_based_on_location


# # model_path = os.path.join(os.path.dirname(__file__), 'models', 'time_4.h5')

# # # Check if the file exists
# # if os.path.exists(model_path):
# #     temperature_model = load_model(model_path)
# # else:
# #     raise FileNotFoundError(f"Model file not found: {model_path}")



# # MongoDB Connection
# client = MongoClient('mongodb://localhost:27017/')
# db = client['farmer']  # Use your actual database name
# collection = db['farmer_data']  # Use your actual collection name

# # views.py


# def login_view(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
#         # Redirect to homepage with the phone number in URL
#         return redirect(f'/home/?phone_number={phone_number}')
#     return render(request, 'login.html')




# def homepage_view(request):
#     phone_number = request.GET.get('phone_number', '')
#     return render(request, 'main.html', {'phone_number': phone_number})



# def profile_view(request):
#     phone_number = request.GET.get('phone_number', '')

#     # Find the user's profile by phone number
#     profile = collection.find_one({'phone_number': phone_number}) or {}

#     return render(request, 'viewprofile.html', {'profile': profile, 'phone_number': phone_number})


def profile_edit(request):
    phone_number = request.GET.get('phone_number', '')

    if request.method == 'POST':
        name = request.POST.get('name')
        contact_number = request.POST.get('contact_number')
        profile_picture = request.POST.get('profile_picture')
        address = request.POST.get('address')
        farm_details = request.POST.get('farm_details')

        # Update profile information for the given phone number
        collection.update_one(
            {'phone_number': phone_number},
            {'$set': {
                'name': name,
                'contact_number': contact_number,
                'profile_picture': profile_picture,
                'address': address,
                'farm_details': farm_details,
            }},
            upsert=True
        )

        # Redirect to the profile view page with phone number
        return redirect(f'/home/profile/?phone_number={phone_number}')

    # Retrieve the profile information for editing
    profile = collection.find_one({'phone_number': phone_number}) or {}

    return render(request, 'profile.html', {'profile': profile, 'phone_number': phone_number})

# def crop_information_view(request):
#     phone_number = request.GET.get('phone_number', '')

#     if request.method == 'POST':
#         crop_name = request.POST.get('crop_name')
#         Location = request.POST.get('location')
#         date = request.POST.get('date')

#         # Update the crop information in the same document based on phone number
#         collection.update_one(
#             {'phone_number': phone_number},
#             {'$push': {  
#                 'crop_details': {
#                     'crop_name': crop_name,
#                     'location': Location,
#                     'date': date,
#                     'submitted_at': timezone.now()
#                 }
#             }},
#             upsert=True
#         )

#         # Redirect to a success page or another page
#         return redirect(f'/home/success/?phone_number={phone_number}')

#     return render(request, 'crop_details.html', {'phone_number': phone_number})



# # def predict_view(request):
# #     if request.method == 'POST':
# #         location = request.POST.get('location')  # Get location from the form

# #         # Pass the location to the AI model function and get predictions
# #         predicted_maxt, predicted_mint, pest_pred_label = predict_based_on_location(location)

# #         # Prepare the response data (You can render a template or return JSON)
# #         response_data = {
# #             'location': location,
# #             'predicted_maxt': predicted_maxt,
# #             'predicted_mint': predicted_mint,
# #             'pest_prediction': pest_pred_label,
# #         }
        
# #         return JsonResponse(response_data)  # Return the result as JSON or render a page
# #     return render(request, 'location_form.html')


# def predict_view(request):
#     if request.method == 'POST':
#         location = request.POST.get('location')  # Get location from the form

#         # Pass the location to the AI model function and get predictions
#         predicted_maxt, predicted_mint, pest_pred_label = predict_based_on_location(location)

#         # Prepare the response data
#         response_data = {
#             'location': location,
#             'predicted_maxt': predicted_maxt,
#             'predicted_mint': predicted_mint,
#             'pest_prediction': pest_pred_label,
#         }
        
#         return JsonResponse(response_data)  # Return the result as JSON
#     return JsonResponse({'error': 'Invalid request method'}, status=400)