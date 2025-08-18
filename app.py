from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def hello():
    return app.send_static_file("index.html")


@app.get("/healthz")
def healthz():
    return jsonify(status="ok"), 200
