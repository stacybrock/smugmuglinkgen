import os, ConfigParser, argparse
from smugpy import SmugMug

SCRIPTPATH = os.path.dirname(os.path.abspath(__file__))

# parse command line arguments
parser = argparse.ArgumentParser(description='Generate links from images in a SmugMug album.')
parser.add_argument('-a', '--album', type=str, help="name of target album")
parser.add_argument('-l', '--list', help="list available albums", action="store_true")
parser.add_argument('-f', '--figure', help="wrap with <figure> tags", action="store_true")
args = parser.parse_args()
if not args.album:
    parser.error("--album argument required")

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
    if args.list:
        print album['Title']
    else:
        if args.album in album['Title']:
            print("Processing %s, %s" % (album['id'], album['Title']))
            images = smugmug.images_get(AlbumID=album['id'], AlbumKey=album['Key'], Heavy=True)
            for image in images['Album']['Images']:
                if image['Width'] > image['Height']:
                    output = '<a href="%s"><img src="%s"/></a>' % (image['OriginalURL'], image['MediumURL'])
                else:
                    output = '<a href="%s"><img src="%s"/></a>' % (image['OriginalURL'], image['LargeURL'])

                if args.figure:
                    output = '<figure>%s</figure>' % output

                print output
