import requests

# Example API endpoint URL
API_ENDPOINT_URL = "https://api.smartnewv2.com/news"

# Optional: If the API requires authentication or API key
headers = {
    "Authorization": "Bearer YOUR_API_KEY"
}

# Make a GET request
response = requests.get(API_ENDPOINT_URL, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the JSON response
    print(response.json())
else:
    print(f"Error: {response.status_code}")
