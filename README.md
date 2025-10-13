# DVWA Vulnerabilities — Lab Writeups & Notes

A collection of vulnerability writeups, reproductions, PoCs, and mitigations for the **Damn Vulnerable Web Application (DVWA)**.  
This repository documents vulnerabilities intentionally present in DVWA.

Official Repo: [https://github.com/digininja/DVWA](https://github.com/digininja/DVWA)

---

## ⚠️ Important — Legal & Safety

> **Only** use DVWA on machines and networks you own or have explicit permission to test (e.g., your Kali VM / home lab).
> Never use the techniques here on public or third-party systems.
> This repo is **educational** — focused on learning, detection, and mitigation.

---

## Purpose

- Provide clear, repeatable writeups for DVWA vulnerabilities that I discovered.
- Serve as a learning resource and personal reference for pentesting practice and writeups.

---

## My Lab Environment

- Host: Kali Linux (VirtualBox)
- Web server: Apache + PHP
- Database: MySQL - MariaDB
- DVWA: latest stable release (clone from [official repo](https://github.com/digininja/DVWA))

---

## DVWA Installation (Kali Linux — lab only)

You can watch this official tutorial suggested by DVWA itself: [https://www.youtube.com/watch?v=WkyDxNJkgQ4](https://www.youtube.com/watch?v=WkyDxNJkgQ4)

---

## Vulnerabilities Documented

Each vulnerability is documented under a folder at /, you can see the list down here:

- [Brute-force](./brute-force/README.md)
- [Command Injection](./command-injection/README.md)
- [CSRF](./csrf/README.md)
- [File Upload](./file-upload/README.md)