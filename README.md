cronmap
=======

A Python-based intelligence gathering tool. `cronmap` allows incident
responders, researchers, engineers, administrators, and others to collaborate
on investigative efforts.

`cronmap` contains features for performing reconnaissance. These include
integrations for third-party tools like Skipfish and nmap, as well as
various open source intelligence sources.

* nmap scan hosts
* brute-force enumerate HTTP servers with Skipfish
* perform simple HTTP enumeration for known URIs with built-in support
* reverse-image search
* search term monitoring

Use
---

`cronmap` currently has been tested on Python 2.7.10.

Set up a virtual environment, install dependencies, and the console UI can be
launched:

```
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python cronmap-console.py
```
