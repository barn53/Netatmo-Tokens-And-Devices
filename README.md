# Netatmo-Tokens-And-Devices
Python scripts to retrieve authorization tokens and device/module IDs from netatmo account

## How to

1) You need to have a netatmo device (focus is solely on the weather station) and a netatmo account.

2) Create an app on this site:
https://dev.netatmo.com/myaccount/createanapp
   - You do not need to add a redirect URI, nor a webhook URL

3) File ```rename_to_secrets.py```
   - Copy the file ```rename_to_secrets.py``` to ```secrets.py```
   - In file ```secrets.py```:
     - Replace the values for email and password according to your account
     - Replace client ID and client secret with the values from the app site

4) Now run ```python get_tokens_devices.py```
   - The following information will be printed to the concole:
     - Access Token
     - Refresh Token
     - All devices with modules and their respective IDs

   - This information is needed to query for measurements
