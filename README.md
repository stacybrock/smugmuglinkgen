# smugmuglinkgen.py

A python script to generate links to images in a SmugMug album.

## Requirements

Developed in python 2.7

First, set up your environment as per `requirements.txt`.

Then, apply for a SmugMug API key: https://api.smugmug.com/api/developer/apply

Enter the API_KEY and API_SECRET into `smugmuglinkgen.conf`.

## Usage

```
usage: smugmuglinkgen.py [-h] [-a ALBUM] [-l] [-f]

Generate links to images in a SmugMug album.

optional arguments:
  -h, --help            show this help message and exit
  -a ALBUM, --album ALBUM
                        name of target album
  -l, --list            list available albums
  -f, --figure          wrap with <figure> tags
```

