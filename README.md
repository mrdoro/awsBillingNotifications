# Periodic notification about AWS billing

This is a simple package that sends a notification to a Slack/MS Teams channel about the billing status of the AWS account.

## Features
* Read billing information from AWS Cost Explorer
* Send notification to Slack/MS Teams over AWS Chatbot


## Requirements

You need configured AWS Chatbot and Slack/MS Teams channel to use this package.
Check example instruction for setting up SNS topic and AWS Chatbot integration [here](https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html).


## Getting Started

To get started with this tool, follow the steps below:

1. Clone this repository to your local machine.
2. Add ARN of the SNS topic to the 'dev.yaml' or 'prod.yaml' file in config folder (depends of your stage).
3. Optionally, you can change the region in the 'serverless.yaml' file.
4. Install Serverless Framework tool to deploy the application to AWS.
5. Install all the dependencies by running `npm install` in the root directory of the project.
6. Deploy the application to AWS by running `serverless deploy --stage dev` or `serverless deploy --stage prod` in the root directory of the project.


## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.