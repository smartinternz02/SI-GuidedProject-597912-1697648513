# SI-GuidedProject-597912-1697648513
To open the Project Developeent Phase folder to access code files:
- Download all zip fiiles, Project Development Phase.7z.001 to .7z.004
- Store them in the same place
- Use 7Zip to extract only the first file i.e. Project Development Phase.7z 001

Since the report button and the print button use free version of external APIs, twilio and IpInfo, these functionalities might not work proprly
To make them work:
- Create twilio account (https://www.twilio.com/login)
- in app.py, under the comment TWILIO, replace account_sid and auth_token with youe personal ids available on their site after creating an account
- under '/send_sms' route, replace 'from' with your personal twilio number which can be found on their website
- Create IpInfo account (https://ipinfo.io/)
- in app.py, under the comment IP INFO, replace 'ACCESS_TOKEN' with your own token which will be available on the webiste after creating an account
