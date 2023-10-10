import time, datetime, requests

start = datetime.datetime.now()
print("Start post method")
response = requests.post(
    "http://127.0.0.1:5000/upscaling/", files={"files": open("lama_300px.png", "rb")}
).json()
file_name = response["file_name"]
task_id = response["task_id"]
print(file_name, task_id)
print("\nStart get method")
status = "PENDING"
while status == "PENDING":
    response = requests.get(f"http://127.0.0.1:5000/upscaling/{task_id}/")
    response = response.json()
    print(response)
    status = response["status"]
    if status == "PENDING":
        time.sleep(10)
print(response)
print("\nSecond get method")
response = requests.get(f"http://127.0.0.1:5000/upscaled/{file_name}/")
print("Done!")
print(f"Время загрузки изображения: {datetime.datetime.now() - start}")
