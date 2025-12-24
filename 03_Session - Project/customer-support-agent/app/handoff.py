import requests
import json

def handoff_to_human(query, response=None):
    webhook_url = "https://discord.com/api/webhooks/1453037334260875330/hrSi6OLehUKMOLprDyHHUygv6amUp-82U0y3QGPrMeWiJUyDsGOp2m3qtyu6By9ZAmnJ"

    payload = {
        "text": f"Escalated query: {query}\nResponse: {response if response else 'N/A'}"
    }
    requests.post(webhook_url, data=json.dumps(payload))
    return "Query escalated to human support."