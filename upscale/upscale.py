import os
import cv2
from celery import Celery
from cv2 import dnn_superres


backend = "redis://127.0.0.1:6379/3"
broker = "redis://127.0.0.1:6379/4"

celery = Celery("app", backend=backend, broker=broker)


@celery.task
def upscale(
    input_path: str,
    output_path: str,
    model_path: str = os.path.join("EDSR_x2.pb"),
):
    """
    :param input_path: путь к изображению для апскейла
    :param output_path:  путь к выходному файлу
    :param model_path: путь к ИИ модели
    :return:
    """

    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel("edsr", 2)
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)


# def example():
#     input_path = os.path.join("lama_300px.png")
#     output_path = "../results\\lama_600px.png"
#     model_path = os.path.join("EDSR_x2.pb")
#     upscale(input_path, output_path, model_path)
#
#
# if __name__ == "__main__":
#     example()
