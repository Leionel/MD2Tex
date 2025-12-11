import requests

try:
    response = requests.post(
        "http://localhost:8000/api/convert",
        json={
            "content": "# Hello World\n\nThis is a test paragraph.\n\n- Item 1\n- Item 2",
            "template_type": "article"
        }
    )
    print("Status Code:", response.status_code)
    print("Response JSON:")
    print(response.json())
except Exception as e:
    print("Error:", e)
