# DVWA - Cryptography

## Description

**Vulnerability:** Cryptography    
**Impact:** Decode the encoded string to get the correct password.

---

## LOW Security Level
In the source code this is how decoding process works:
```php
$decoded = xor_this (base64_decode ($password), $key);
```
First Base64 Decode the password then decode with XOR and the key is `wachtwoord`. I use [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)XOR(%7B'option':'UTF8','string':'wachtwoord'%7D,'Standard',false)&input=TGc0V0dsUVpDaGhTRkJZU0VCOGJCUXRQR3hkTlFTd0VIUkVPQVFZPQ) to decode this encoded string:

![Guide image](./screenshots/1.png)

Result:
```
Your new password is: Olifant
```

![Guide image](./screenshots/2.png)

## MEDIUM Security Level
The tokens are encrypted using an Electronic Code Book based algorithm (AES-128-ECB). aes-128-ebc is a 128 bit block cipher. 128 bits is 16 bytes, but to make things human readable, the bytes are represented as hex characters meaning each byte is two characters. This gives you a block size of 32 characters. 

Let's broken down Sooty:

```
Sooty:

e287af752ed3f9601befd45726785bd9 <- Username
b85bb230876912bf3c66e50758b222d0 <- Expiry
837d1e6b16bfae07b776feb7afe57630 <- Level
5aec34b41499579d3fb6acc8dc92fd5f <- Bio
cea8743c3b2904de83944d6b19733cdb
48dd16048ed89967c250ab7f00629dba
```

The app requires us to ` Manipulate the session tokens you have captured to log in as Sweep with admin privileges.` so we can combine the Username of Sweep, Expiry of Soo, Level admin from Sooty and Bio of Sweep.

```
3061837c4f9debaf19d4539bfa0074c1 <- Sweep as username
174d4b2659239bbc50646e14a70becef <- Soo's expiry time
837d1e6b16bfae07b776feb7afe57630 <- Sooty's admin privileges
caeb574f10f349ed839fbfd223903368 <- Finish off with Sweep's bio
873580b2e3e494ace1e9e8035f0e7e07
```

Final token:
```
3061837c4f9debaf19d4539bfa0074c1174d4b2659239bbc50646e14a70becef837d1e6b16bfae07b776feb7afe57630caeb574f10f349ed839fbfd223903368873580b2e3e494ace1e9e8035f0e7e07
```

![Guide image](./screenshots/3.png)

## HIGH Security Level
It is suggested to go to this site to find the answer https://www.nccgroup.com/research-blog/cryptopals-exploiting-cbc-padding-oracles/


## Resources
- AES-ECB Padding Attack
- Implementing and breaking AES ECB
- Wikipedia - Block cipher mode of operation
- Cryptopals: Exploiting CBC Padding Oracles - Best article
- [Crypto] PKCS#7 padding
- Padding oracle attack
- Oracle Padding Attack
- The Padding Oracle Attack
- Wikipedia - Padding (cryptography)
- CyberChef
- XOR Encryption Algorithm
- XOR Cipher
- Video walk-through by CryptoCat
