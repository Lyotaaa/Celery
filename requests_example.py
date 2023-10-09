# import requests
# import os
# import time
#
#
# response = requests.post(
#     "http://127.0.0.1:5000/upscale",
#     json={
#         # "files": open("upscale/lama_300px.png", "rb"),
#         "in_files": os.path.join("upscale", "lama_300px.png"),
#         "out_files": os.path.join("results", "lama_600px.png"),
#         # "out_files": os.path.join("../results", "lama_600px.png"),
#     },
# ).json()
# print(response)
# task_id = response.get("task_id")
# print(task_id)
#
# while True:
#     response = requests.get(f"http://127.0.0.1:5000/tasks/{task_id}").json()
#     print(response)
#     time.sleep(1.0)
#     if response["status"] == "SUCCESS":
#         print("Success!")
#         break

import datetime
import requests
import time

start = datetime.datetime.now()
print('Start post method')
response = requests.post('http://127.0.0.1:5000/upscale', files={
    'file': open('upscale/lama_300px.png', 'rb')
}).json()
task_id = response['task_id']
print(task_id)
print('\nStart get method')
status = 'PENDING'
while status == 'PENDING':
    response = requests.get(f'http://127.0.0.1:5000/tasks/{task_id}')
    response = response.json()
    print(response)
    status = response['status']
    if status == 'PENDING':
        time.sleep(10)
print(response)
print('\nSecond get method')
# response = requests.get(f'http://127.0.0.1:5000/upscaled/{file_name}/')
# print('Done!')
# print(f'Время загрузки изображения: {datetime.datetime.now() - start}')