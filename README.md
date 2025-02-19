📌 How to Use
- Install dependencies using pip install selenium.
- Download and install ChromeDriver, ensuring it matches your Chrome version.
- Set up AWS credentials with appropriate permissions for accessing AWS Lambda.
- Place chromedriver.exe in the project folder and update the script with the correct path if necessary.
- Run the script using python index.py and manually enter your MFA code when prompted.
- Wait for the script to process all Lambda functions, navigating through multiple pages as needed.
- Once completed, find the extracted data in AWS_QA/lambda_functions.csv on your desktop.
- To stop the script safely, press Ctrl + C, ensuring all collected data is saved before exit.
- Open the CSV file to view Lambda details including name, last modified date, runtime, layers, API endpoint, and HTTP method.

This tool provides an efficient way to audit and document AWS Lambda functions without manual effort.
