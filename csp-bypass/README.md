# DVWA - CSP Bypass

## Description

**Vulnerability:** CSP Bypass    
**Impact:** Bypass CSP policy and inject our desired Javascript code.

---

## LOW Security Level
This Security Level allow these scripts:
```php
$headerCSP = "Content-Security-Policy: script-src 'self' https://pastebin.com hastebin.com www.toptal.com example.com code.jquery.com https://ssl.google-analytics.com https://digi.ninja ;"; // allows js from self, pastebin.com, hastebin.com, jquery, digi.ninja, and google analytics.
```
As it allows `https://digi.ninja` so we can use `https://digi.ninja/dvwa/cookie.js`. Result:

![Guide image](./screenshots/1.png)

## MEDIUM Security Level
The CSP now is new
```php
$headerCSP = "Content-Security-Policy: script-src 'self' 'unsafe-inline' 'nonce-TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=';";
```
It allows script with `nonce: TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=` so the payload is:
```html
<script nonce="TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=">alert(document.cookie)</script>
```

![Guide image](./screenshots/2.png)

## HIGH Security Level
This HIGH Level use another `jsonp.php` to execute the code and it use a `callback` query param to execute so we can use Burp Suite to intercept the request when click `Solve the sum`, change `?callback=solveSum` to `?callback=alert(document.cookie)`

In Burp Suite turn Intercept on:

![Guide image](./screenshots/3.png)

Result:

![Guide image](./screenshots/4.png)


## Resources
- [Content Security Policy Reference](https://content-security-policy.com/)
- [Mozilla Developer Network - CSP: script-src](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [Mozilla Security Blog - CSP for the web we have](https://blog.mozilla.org/security/2014/10/04/csp-for-the-web-we-have/)
