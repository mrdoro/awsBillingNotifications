import boto3
from datetime import datetime, timedelta
import logging
from src.common.send_notification import send_notification
from calendar import monthrange

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    client = boto3.client('ce', region_name='us-east-1')  # Create a Cost Explorer client
    
    # Get the current date
    current_date = datetime.now()

    # Subtract an hour to adjust for UTC+1
    current_date -= timedelta(hours=1)

    # Define the filter to exclude costs associated with AWS credits
    filter = {
        "Dimensions": {
            "Key": "RECORD_TYPE",
            "Values": ["Usage", "Tax", "Other out-of-cycle charges"]
        }
    }
    
    # Format the current date to the required format
    start_date = current_date.strftime('%Y-%m-01')  # Start of the current month
    end_date = current_date.strftime('%Y-%m-%d')  # Current date

    logger.info(f"Getting cost from {start_date} to {end_date}")

    _, last_day = monthrange(current_date.year, current_date.month)
    end_of_month = current_date.replace(day=last_day).strftime('%Y-%m-%d')


    # Get the cost from the start of the month to today
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='DAILY',
        Filter=filter,
        Metrics=[
            'BlendedCost',
        ]
    )
    total_cost = sum(float(day['Total']['BlendedCost']['Amount']) for day in response['ResultsByTime'])
    total_cost = round(total_cost, 2)

    logger.info(f"Getting forecast from {end_date} to {end_of_month}")
    # Get the forecasted cost from today to the end of the month
    if current_date.date() < datetime.strptime(end_of_month, '%Y-%m-%d').date():
        forecast_response = client.get_cost_forecast(
            TimePeriod={
                'Start': end_date,  # Current date needed for forecast
                'End': end_of_month
            },
            Metric='BLENDED_COST',
            Filter=filter,
            Granularity='DAILY'
        )
        logger.info(f"Forecast response: {forecast_response}")
        forecast_cost = float(forecast_response['Total']['Amount'])
        forecast_cost = round(forecast_cost, 2)
    else:
        forecast_cost = 0

    total_forecast = round(total_cost + forecast_cost, 2)
    

    payload = {
        'current_date': end_date,
        'total_cost': str(total_cost),
        'forecast_cost': str(total_forecast)
    }

    logger.info("Sending notification...")
    send_notification(payload)
    
    logger.info(f"The total cost for this month up to today is ${total_cost}, and the forecast for the rest of the month is ${forecast_cost}")