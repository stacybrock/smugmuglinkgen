# smugmuglinkgen.py

A python script to generate links to images in a SmugMug album.

## Requirements

Developed in python 2.7

1. Set up environment using `requirements.txt`.
1. Copy `smugmuglinkgen.conf-dist` to `smugmuglinkgen.conf`.
1. Edit `smugmuglinkgen.conf` and change `smugmug_user` to your SmugMug username.
1. Apply for a SmugMug API key: https://api.smugmug.com/api/developer/apply
1. Edit `smugmuglinkgen.conf` and update `api_key` and `api_secret` with the correct values.

## Usage

```
smugmuglinkgen.py

Usage:
    smugmuglinkgen.py list
    smugmuglinkgen.py album <albumname> generate ( links | figures | bbcode )
    smugmuglinkgen.py (-h | --help)
    smugmuglinkgen.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
```
