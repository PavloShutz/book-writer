![check-code-coverage](https://img.shields.io/badge/code--coverage-100%25-brightgreen)

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
3. Read other people's books.

## How to install it?
```
git clone https://github.com/PavloShutz/book-writer.git
```

## Other preparations
- Initialize database: ```flask --app book_writer init-db```
- Specify secret keys in config.py: 
```python
SECRET_KEY = "YOUR SECRET KEY HERE"
WTF_CSRF_SECRET_KEY = "YOUR SECRET KEY HERE"
```
