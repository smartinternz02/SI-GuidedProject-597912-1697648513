# SI-GuidedProject-597912-1697648513
BEFORE running app.py, download the model h5 file from here: https://drive.google.com/file/d/1x2HQSPTcQxXrEg3EsB1sWHIqOoeWWpoy/view?usp=sharing

Access the dataset from the follwoing link: https://www.kaggle.com/datasets/odins0n/ucf-crime-dataset

Since the report button and the print button use free version of external APIs, twilio and IpInfo, these functionalities might not work proprly
To make them work:
- Create twilio account (https://www.twilio.com/login)
- in app.py, under the comment TWILIO, replace account_sid and auth_token with youe personal ids available on their site after creating an account
- under '/send_sms' route, replace 'from' with your personal twilio number which can be found on their website
- Create IpInfo account (https://ipinfo.io/)
- in app.py, under the comment IP INFO, replace 'ACCESS_TOKEN' with your own token which will be available on the webiste after creating an account
