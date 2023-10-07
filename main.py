import uuid
import os
from flask import Flask, request, jsonify
from flask.views import MethodView
from celery.result import AsyncResult
from upscale import upscale, celery


app = Flask("app")
app.config["UPLOAD_FOLDER"] = "files"
celery.conf.update(app.config)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask


class UpscaleView(MethodView):
    def get(self, task_id):
        task = AsyncResult(task_id, app=celery)
        return jsonify({"status": task.status, "result": task.result})

    def post(self):
        input_path, output_path = self.save_image()
        task = upscale.delay(input_path, output_path)
        return jsonify({"task_id": task.id, "file": output_path})

    def save_image(self):
        image = request.files.get("files")
        extension = image.filename.split(".")[-1]
        input_path = os.path.join("files", f"lama_300px.{extension}")
        output_path = os.path.join("files", f"lama_600px.{extension}")
        image.save(input_path)
        return input_path, output_path


class ProcessedView(MethodView):
    def get(self, file):
        status = "ERROR"
        if file:
            status = "SUCCESS"
        return jsonify(
            {"status": status, "result_path": os.path.join("files", f"{file}")}
        )


upscale_view = UpscaleView.as_view("upscale")
processed_view = ProcessedView.as_view("processed")

app.add_url_rule("/tasks/<string:task_id>", view_func=upscale_view, methods=["GET"])
app.add_url_rule("/processed/<string:file>", view_func=processed_view, methods=["GET"])
app.add_url_rule("/upscale/", view_func=upscale_view, methods=["POST"])


if __name__ == "__main__":
    app.run()
