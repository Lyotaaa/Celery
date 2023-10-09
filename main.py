import os
from upscale.upscale import celery, upscale
from flask import Flask, request, jsonify
from flask.views import MethodView
from celery.result import AsyncResult

app_name = "app"
app = Flask(app_name)
app.config["UPLOAD_FOLDER"] = "results"
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
        input_path, output_path = self.get_image()
        task = upscale.delay(input_path, output_path)
        return jsonify(
            {
                "task_id": task.id,
            }
        )

    def get_image(self):
        in_files = request.json["in_files"]
        out_files = request.json["out_files"]
        return in_files, out_files

    # def get_image(self):
    #     image = request.files.get("files")
    #     extension = image.filename.split(".")[-1]
    #     input_path = os.path.join("results", f"lama_300px.{extension}")
    #     output_path = os.path.join("results", f"lama_600px.{extension}")
    #     image.save(input_path)
    #     return input_path, output_path


class ProcessedView(MethodView):
    def get(self, filename):
        status = None
        if status == "SUCCESS":
            return jsonify({"status": status, "path_in_file": os.path.join("files", f"")})


upscale_view = UpscaleView.as_view("upscale")
processed_view = ProcessedView.as_view("processed")
app.add_url_rule("/upscale", view_func=upscale_view, methods=["POST"])
app.add_url_rule("/tasks/<string:task_id>", view_func=upscale_view, methods=["GET"])
app.add_url_rule(
    "/processed/<string:filename>", view_func=processed_view, methods=["GET"]
)

if __name__ == "__main__":
    app.run()
