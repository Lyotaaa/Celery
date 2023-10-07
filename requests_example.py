import requests
import time


response = requests.post(
    "http://127.0.0.1:5000/upscale/", files={"files": open("lama_300px.png", "rb")}
).json()
print(response)
task_id = response.get("task_id")
print(task_id)

while True:
    response = requests.get(f"http://127.0.0.1:5000/tasks/{task_id}").json()
    print(response)
    time.sleep(0.1)
    if response["status"] == "SUCCESS":
        print("Success!")
        break
