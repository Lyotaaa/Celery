import os
import cv2
from cv2 import dnn_superres
from celery import Celery, ContextTask
from flask import Flask, jsonify, request
from flask.views import MethodView
from celery.result import AsyncResult


'''Парамтры для Flask и Celery'''
app_name = 'app'
app = Flask(app_name)
app.comfig["UPLOAD_PATH"] = "result"
celery = Celery("app", backend="redis://127.0.0.1:6379/1", broker="redis://127.0.0.1:6379/2")
celery.conf.update(app.config)

'''Волшебная функция'''
class Context(celery.task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

'''Обработка фотографии'''
@celery.task()
def upscale(input_path: str, output_path: str, model_path: str = 'EDSR_x2.pb') -> None:
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

