import requests
import time
import random

# API endpoint
API_URL = "http://127.0.0.1:5000/data"  # Replace with your API's URL if hosted elsewhere

# Function to generate mock data
def generate_mock_data():
    return {
        "metal": random.randint(0, 100),  # Random metal value (0-100)
        "plastic": random.randint(0, 100)  # Random plastic value (0-100)
    }

# Function to post data to the API
def post_data():
    print('entrou')
    mock_data = generate_mock_data()
    print('entrou2')
    try:
        response = requests.post(API_URL, json=mock_data)
        print('entrou3')
        if response.status_code == 200:
            print(f"Data posted successfully: {mock_data}")
        else:
            print(f"Failed to post data. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error posting data: {e}")

# Main loop to post data every 1 minute
if __name__ == "__main__":
    while True:
        post_data()
        time.sleep(60)  # Wait for 60 seconds before posting again