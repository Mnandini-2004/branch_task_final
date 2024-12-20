import requests

api_url = "http://127.0.0.1:5000/predict"

# Sample input data
input_data = {
    "application_at": 0.097039,
    "gps_fix_at": 0.018527,
    "server_upload_at": 0.018987,
    "age": 0.066432,
    "cash_incoming_30days": -0.093135
}

# Send POST request to the Flask API
response = requests.post(api_url, json=input_data)

# Print the response from the API
print("Status Code:", response.status_code)
print("Response Text:", response.text)

try:
    print("Response JSON:", response.json())
except Exception as e:
    print("Error parsing JSON:", e)
