import requests


res = requests.get("https://www.youtube.com/watch?v=2wqpy036z24")

print(res.text)
