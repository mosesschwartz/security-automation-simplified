import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/status")
def status():
    return "up"


@app.route("/splunk_webhook", methods=["POST"])
def splunk_webhook():
    webhook_payload = request.get_json()
    with open("splunk_webhook.json", "w") as f:
        json.dump(webhook_payload, f, indent=4)
    return "success"


app.run(host="0.0.0.0", port=80, debug=False)
