import requests

import settings


def get_file_scan_report(file_hash):
    vt_url = "https://www.virustotal.com/vtapi/v2/file/report"
    params = {
        "apikey": settings.vt_api_key,
        "resource": file_hash,
    }
    response = requests.get(vt_url, params=params)
    return response.json()
