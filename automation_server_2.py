import json

from flask import Flask, request
from jira import JIRA

import settings

app = Flask(__name__)


@app.route("/status")
def status():
    return "up"


@app.route("/splunk_webhook", methods=["POST"])
def splunk_webhook():
    webhook_payload = request.get_json()
    ticket = create_jira_issue(
        webhook_payload["search_name"], webhook_payload
    )
    return "success"


def create_jira_issue(alert_name, alert_body):
    j = JIRA(
        settings.jira_url,
        basic_auth=(settings.username, settings.password),
    )
    j.create_issue(
        project=settings.jira_project,
        summary="SplunkAlert: {}".format(alert_name),
        description=json.dumps(alert_body),
        issuetype="Incident",
    )


app.run(host="0.0.0.0", port=80, debug=False)
