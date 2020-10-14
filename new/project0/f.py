import requests

response = requests.get('http://google.com/search?q=hello')
print(response.status_code)
