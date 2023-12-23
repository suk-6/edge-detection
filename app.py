import os
import time
import random
import base64
import os.path as osp
from io import BytesIO
from PIL import Image
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
root = osp.dirname(osp.abspath(__file__))
tmpPath = osp.join(root, "tmp")

if not osp.exists(tmpPath):
    os.mkdir(tmpPath)


def imageToBase64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)

    return base64.b64encode(buffered.getvalue()).decode()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        f = request.files["file"]
        id = f"{datetime.timestamp(datetime.now())}.{random.randint(0, 1000)}"
        filename, extention = osp.splitext(f.filename)
        basePath = osp.join(tmpPath, id)

        savePath = osp.join(tmpPath, f"{id}_original{extention}")
        f.save(savePath)

        os.system(f"python laplacian.py {basePath} {extention} > /dev/null &")

        time.sleep(2)
        return redirect(url_for("view", id=id))

    return render_template("index.html")


@app.route("/view/<id>")
def view(id):
    return render_template("view.html", id=id)


@app.route("/data/<id>")
def getData(id):
    basePath = osp.join(tmpPath, id)

    if osp.exists(f"{basePath}_result.gif"):
        return jsonify(
            {
                "id": id,
                "refresh": False,
                "result": imageToBase64(Image.open(f"{basePath}_result.gif")),
            }
        )

    gray = imageToBase64(Image.open(f"{basePath}_gray.jpg"))
    edge = imageToBase64(Image.open(f"{basePath}_edge.jpg"))
    blur = imageToBase64(Image.open(f"{basePath}_blur.jpg"))

    return jsonify(
        {"id": id, "refresh": True, "gray": gray, "edge": edge, "blur": blur}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
