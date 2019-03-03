import json

from flask import Flask, request
from jira import JIRA

import settings

app = Flask(__name__)


@app.route("/status")
def status():
    return "up"


@app.route("/jira_mockscan_created_webhook", methods=["POST"])
def mockscan_created():
    jira_webhook = request.get_json()
    jira_desc = jira_webhook["issue"]["fields"]["description"]
    issue_key = jira_webhook["issue"]["key"]
    splunk_alert = json.loads(jira_desc)
    user = splunk_alert["result"]["user"]
    md5 = splunk_alert["result"]["md5"]
    comment = "MockScan Alert: User={} MD5={}".format(user,md5)
    jira_comment(issue_key, comment)
    return "success"


def jira_comment(issue_key, comment):
    j = JIRA(
        settings.jira_url,
        basic_auth=(settings.username, settings.password),
    )
    issue = j.issue(issue_key)
    j.add_comment(issue, comment)


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
