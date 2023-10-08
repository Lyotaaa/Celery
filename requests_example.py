import requests
import os
import time


response = requests.post(
    "http://127.0.0.1:5000/upscale",
    json={
        # "files": open("upscale/lama_300px.png", "rb"),
        "in_files": os.path.join("upscale", "lama_300px.png"),
        "out_files": "../results\\lama_600px.png",
        # "out_files": os.path.join("../results", "lama_600px.png"),
    },
).json()
print(response)
task_id = response.get("task_id")
print(task_id)

# while True:
#     response = requests.get(f"http://127.0.0.1:5000/tasks/{task_id}").json()
#     print(response)
#     time.sleep(1.0)
#     if response["status"] == "SUCCESS":
#         print("Success!")
#         break
