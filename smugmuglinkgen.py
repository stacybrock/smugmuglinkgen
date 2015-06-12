"""smugmuglinkgen.py

Usage:
    smugmuglinkgen.py list
    smugmuglinkgen.py album <albumname> generate ( links | figures | bbcode )
    smugmuglinkgen.py (-h | --help)
    smugmuglinkgen.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
"""
import os, ConfigParser
from docopt import docopt
from smugpy import SmugMug

SCRIPTPATH = os.path.dirname(os.path.abspath(__file__))

# parse command line arguments
arguments = docopt(__doc__, version='smugmuglinkgen.py 0.1')

# parse config file
config = ConfigParser.ConfigParser()
config.read(SCRIPTPATH+'/smugmuglinkgen.conf')
API_KEY = config.get('main', 'api_key')
API_SECRET = config.get('main', 'api_secret')
TOKEN = config.get('main', 'token')
SECRET = config.get('main', 'secret')
USERNAME = config.get('main', 'smugmug_user')

# set up smugmug API
smugmug = SmugMug(api_key=API_KEY, oauth_secret=API_SECRET, app_name="get_gallery_links")

# oauth
if TOKEN and SECRET:
    smugmug.set_oauth_token(TOKEN, SECRET)
    response = smugmug.auth_checkAccessToken()
    #print response
else:
    smugmug.auth_getRequestToken()
    raw_input("Authorize app at %s\n\nPress Enter when complete.\n" % (smugmug.authorize(access='Full')))
    response = smugmug.auth_getAccessToken()
    print("  token: %s" % response['Auth']['Token']['id'])
    print("  secret: %s" % response['Auth']['Token']['Secret'])
    print "Enter these values into smugmuglinkgen.conf to skip this auth process the next time around."

# the real work starts here
albums = smugmug.albums_get(NickName=USERNAME)
for album in albums['Albums']:
    if arguments['list']:
        print album['Title']
    else:
        if arguments['<albumname>'] in album['Title']:
            print("Processing %s, %s" % (album['id'], album['Title']))
            images = smugmug.images_get(AlbumID=album['id'], AlbumKey=album['Key'], Heavy=True)
            for image in images['Album']['Images']:
                original_url = image['OriginalURL']

                if image['Width'] > image['Height']:
                    display_url = image['MediumURL']
                else:
                    display_url = image['LargeURL']

                if arguments['bbcode']:
                    output = '[url=%s][img]%s[/img][/url]' % (original_url, display_url)
                else:
                    output = '<a href="%s"><img src="%s"/></a>' % (original_url, display_url)
                    if arguments['figures']:
                        output = '<figure>%s</figure>' % output

                print output
