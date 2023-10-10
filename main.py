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



def get_file_name(file: str):
    return file[len(app.config['UPLOAD_FOLDER']) + 1:]

class UpscaleView(MethodView):
    def post(self):
        orig_file, res_file = self.save_image()
        task = upscale.delay(orig_file, res_file)
        return jsonify({
            'task_id': task.id,
            #'file_name': get_file_name(res_file)
        })

    def get(self, task_id):
        task = AsyncResult(task_id, app=celery)
        return jsonify({
            'status': task.status,
        })


    def save_image(self):
        image = request.files.get('file')
        extension, name = image.filename.split('.')[-1], image.filename.split('.')[0]
        orig_file = os.path.join('files', f'{name}.{extension}')
        res_file = os.path.join('files', f'{name}_upscaled.{extension}')
        image.save(orig_file)
        # image.save(res_file)
        return orig_file, res_file


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


