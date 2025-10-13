# DVWA - Weak Session IDs

## Description

**Vulnerability:** Weak Session IDs    
**Impact:** Session IDs may be guessed to gain access as other accounts.

---

## LOW Security Level
This level has really simple code:
```php
<?php

$html = "";

if ($_SERVER['REQUEST_METHOD'] == "POST") {
    if (!isset ($_SESSION['last_session_id'])) {
        $_SESSION['last_session_id'] = 0;
    }
    $_SESSION['last_session_id']++;
    $cookie_value = $_SESSION['last_session_id'];
    setcookie("dvwaSession", $cookie_value);
}
?>
```

The `dvwaSession` cookie will simply increases 1 when we click the `Generate` button.

![Guide image](./screenshots/1.png)

## MEDIUM Security Level
This MEDIUM Security Level is also simple it take `time()` value which is the current Unix timestamp and set that to `dvwaSession` cookie value:
```php
<?php

$html = "";

if ($_SERVER['REQUEST_METHOD'] == "POST") {
    $cookie_value = time();
    setcookie("dvwaSession", $cookie_value);
}
?>
```

## HIGH Security Level
This is the source code of HIGH Security Level:
```php
<?php

$html = "";

if ($_SERVER['REQUEST_METHOD'] == "POST") {
    if (!isset ($_SESSION['last_session_id_high'])) {
        $_SESSION['last_session_id_high'] = 0;
    }
    $_SESSION['last_session_id_high']++;
    $cookie_value = md5($_SESSION['last_session_id_high']);
    setcookie("dvwaSession", $cookie_value, time()+3600, "/vulnerabilities/weak_id/", $_SERVER['HTTP_HOST'], false, false);
}

?>
```

This is what it looks like `c81e728d9d4c2f636f067f89cc14862c`:

![Guide image](./screenshots/2.png)

Let's reverse this by decrypt MD5 (I use CrackStation):

![Guide image](./screenshots/3.png)

This is the value of `last_session_id_high` so every time we click the higher value will be increase by one and MD5 hash.