![check-tests-passing](https://img.shields.io/badge/tests--passing-100%25-brightgreen)

<picture style="width: 30px; height: auto;">
  <source media="(prefers-color-scheme: dark)" srcset="https://cdn-icons-png.flaticon.com/128/3839/3839574.png">
  <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="https://cdn-icons-png.flaticon.com/128/3839/3839574.png">
</picture> 

# book-writer

## What is it?

Book writer web application allows you to write your book online. Though it seems like a post creating app, in future there will be added some specific features that allows you to create book. 

## Why it is cool?
1. Easy registration and loginization.
2. Cool book editor.
3. Read other people's books and rate them.
4. See users statistics

## How to install it?
* #### Clone this repository
```commandline
git clone https://github.com/PavloShutz/book-writer.git
```
* #### Install all requirements
```commandline
pip install -r requirements.txt
```

## Other preparations
- Initialize database:
```commandline
flask init-db
```
- Specify secret keys in config.py: 
```python
SECRET_KEY = "YOUR SECRET KEY HERE"
WTF_CSRF_SECRET_KEY = "YOUR SECRET KEY HERE"
```
