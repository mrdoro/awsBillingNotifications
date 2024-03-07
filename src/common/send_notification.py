import boto3
import json
import os

sns = boto3.client('sns')

SNS_TOPIC = os.environ['SNS_TOPIC']

def send_notification(payload):
    print("Payload received by send_notification: ", payload)
    description = (f"The current state of the billing for today is ${payload['total_cost']}\n"
               f"Forecast for this month is ${payload['forecast_cost']}")
    message = {
            "version": "1.0",
            "source": "custom",
            "content": {
                "textType": "client-markdown",
                "title": f"The billing status for {payload['current_date']}",
                "description": description,
                "keywords": [
                    "Billing",
                    "Information",
                    "SRE"
                ]
            },
            "metadata": {
                "summary": "Current total costs for this month up to today is: $" + payload['total_cost'],
                "relatedResources": [
                    payload['total_cost'],
                ],
                "additionalContext": {
                    "priority": "Warning"
                }
            }
    }

    response = sns.publish(
            TopicArn= SNS_TOPIC,
            Message=json.dumps(message)
    )

    print("Notification sent successfully: " + json.dumps(response))