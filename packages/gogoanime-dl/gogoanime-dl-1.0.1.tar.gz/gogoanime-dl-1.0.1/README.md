
# Gogoanime-DL
[![PyPI](https://img.shields.io/pypi/v/gogoanime-dl.svg)](https://pypi.python.org/pypi/gogoanime-dl)
![Python Versions](https://img.shields.io/pypi/pyversions/gogoanime-dl.svg)

![License](https://img.shields.io/github/license/AuraMoon55/gogoanime-dl.svg)

Gogoanime Anime Downloader

- An Anime Scraping Package that finds anime from gogoanime and helps in downloading anime


```bash
$ python3 -m pip install gogoanime-dl
```

## Example
```python
from gogoanime import GoGo

Anime = GoGo()
Anime.search("One Piece")
```

## Custom Download Location Example
```python
from gogoanime import GoGo

Anime = GoGo(download_path="/path-to-folder")
#         OR
Anime = GoGo("/path-to-folder")
#By default download_path is downloads
```
