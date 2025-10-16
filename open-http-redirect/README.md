# DVWA - Open HTTP Redirect

## Description

**Vulnerability:** Open HTTP Redirect    
**Impact:** Taking advantage of redirects to trick users go to other websites.

---

## LOW Security Level
The source code in `vulnerabilities/open_redirect/source/low.php` is:
```php
if (array_key_exists ("redirect", $_GET) && $_GET['redirect'] != "") {
    header ("location: " . $_GET['redirect']);
    exit;
}

http_response_code (500);
?>
<p>Missing redirect target.</p>
<?php
exit;
```
No checks so we can leverage this if you check the url of Quote 1 and Quote 2 it is: `source/low.php?redirect=info.php?id=1`, so we can use this `redirect` query param to redirect users to whatever page we want:
```
http://localhost/DVWA/vulnerabilities/open_redirect/source/low.php?redirect=https://jameskaois.com
```

## MEDIUM Security Level
The source code now checks `http` and `https`:
```php
if (array_key_exists ("redirect", $_GET) && $_GET['redirect'] != "") {
    if (preg_match ("/http:\/\/|https:\/\//i", $_GET['redirect'])) {
        http_response_code (500);
        ?>
        <p>Absolute URLs not allowed.</p>
        <?php
        exit;
    } else {
        header ("location: " . $_GET['redirect']);
        exit;
    }
}

http_response_code (500);
?>
<p>Missing redirect target.</p>
<?php
exit;
```
We can still force users to redirect without the use of `http` and `https`:
```
/DVWA/vulnerabilities/open_redirect/source/low.php?redirect=//jameskaois.com
```

## HIGH Security Level
The redirect now just allows `info.php`:
```php
if (array_key_exists ("redirect", $_GET) && $_GET['redirect'] != "") {
    if (strpos($_GET['redirect'], "info.php") !== false) {
        header ("location: " . $_GET['redirect']);
        exit;
    } else {
        http_response_code (500);
        ?>
        <p>You can only redirect to the info page.</p>
        <?php
        exit;
    }
}

http_response_code (500);
?>
<p>Missing redirect target.</p>
<?php
exit;
```
This check just need `info.php` exists in `redirect` query param so we can just need to add a trick `info.php`:
```
http://localhost/DVWA/vulnerabilities/open_redirect/source/high.php?redirect=//jameskaois.com?trick=info.php
```

## Resources
- [OWASP Unvalidated Redirects and Forwards Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)
- [WSTG - Testing for Client-side URL Redirect](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/11-Client-side_Testing/04-Testing_for_Client-side_URL_Redirect)
- [Mitre - CWE-601: URL Redirection to Untrusted Site ('Open Redirect')](https://cwe.mitre.org/data/definitions/601.html)
