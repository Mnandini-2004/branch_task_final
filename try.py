import requests
import json
from datetime import datetime
import time

class LoanPredictionClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        
    def check_health(self):
        """Check if the API service is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.json()
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}

    def predict_loan(self, user_data):
        """Make a loan prediction request"""
        try:
            response = requests.post(
                f"{self.base_url}/predict",
                json=user_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "status": "error",
                    "message": f"Request failed with status code: {response.status_code}",
                    "details": response.json()
                }
                
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}

# Example usage
if __name__ == "__main__":
    # Initialize the client
    client = LoanPredictionClient()
    
    # Check if service is healthy
    print("Checking API health...")
    health_status = client.check_health()
    print(json.dumps(health_status, indent=2))
    
    # Example data
    test_cases = [
        {
            # Valid data
            "user_id": 1,
            "application_at": "2023-12-20T09:08:50",
            "gps_fix_at": "2023-12-20T09:37:20",
            "server_upload_at": "2023-12-20T09:43:42",
            "age": 42,
            "cash_incoming_30days": 8988.12
        },
        {
            # Different user data
            "user_id": 2,
            "application_at": "2023-12-20T15:30:00",
            "gps_fix_at": "2023-12-20T15:25:00",
            "server_upload_at": "2023-12-20T15:35:00",
            "age": 35,
            "cash_incoming_30days": 6500.00
        },
        {
            # Incomplete data to test error handling
            "user_id": 3,
            "application_at": "2023-12-20T10:00:00",
            "age": 28
        }
    ]
    
    # Make predictions for each test case
    for i, test_data in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print("Input data:")
        print(json.dumps(test_data, indent=2))
        
        print("\nMaking prediction request...")
        result = client.predict_loan(test_data)
        print("Response:")
        print(json.dumps(result, indent=2))
        
        # Add slight delay between requests
        time.sleep(1)

# Function for single prediction
def make_single_prediction(user_data):
    """
    Make a single prediction request
    
    Args:
        user_data (dict): Dictionary containing user loan application data
    Returns:
        dict: Prediction response
    """
    url = "http://localhost:5000/predict"
    
    try:
        response = requests.post(
            url,
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )
        return response.json()
    except requests.RequestException as e:
        return {"status": "error", "message": str(e)}

# Example of single prediction usage
if __name__ == "__main__":
    # Single prediction example
    single_user_data = {
        "user_id": 5,
        "application_at": datetime.now().isoformat(),
        "gps_fix_at": datetime.now().isoformat(),
        "server_upload_at": datetime.now().isoformat(),
        "age": 45,
        "cash_incoming_30days": 7500.00
    }
    
    print("\nMaking single prediction:")
    result = make_single_prediction(single_user_data)
    print(json.dumps(result, indent=2))