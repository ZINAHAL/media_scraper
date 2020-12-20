import requests
from bs4 import BeautifulSoup
import validators
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from helpers import *


origin = input( "Enter the website's url [ example: http://www.abc.ie/ ]: " )

if not validators.url( origin ):
    sys.exit( "The entered url is not valid. Please try again!" )

try:
    response = requests.get( origin )
except requests.ConnectionError:
    sys.exit( "The given website name doesn't exsist." )

storage_path = create_directory_to_store_media()
if storage_path is None:
    sys.exit()

soup = BeautifulSoup( response.text, 'html.parser' )
nav_a_tags = soup.nav.ul.find_all( 'a' )
a_hrefs = [ a['href'] for a in nav_a_tags ]
found_media_urls = []
print("Working....")
if a_hrefs[0] == origin:
    bucket = a_hrefs
    for nav_href in bucket:
        a_hrefs = a_hrefs + get_all_hrefs( nav_href, origin )

    # Removing all duplicate values
    a_hrefs = list( dict.fromkeys( a_hrefs ) )
    print("Digging....")

    for href in a_hrefs:
        found_media_urls.extend( get_media_paths( href ) )
else:
    for href in a_hrefs:
        found_media_urls.extend( get_media_paths( origin + clean_path( href ) ) )
    
    found_media_urls = [ origin + clean_path( path ) for path in found_media_urls ]

#removing duplicate values from the list
found_media_urls = list( dict.fromkeys( found_media_urls ) )

print("Got it....")
with tqdm( total=len( found_media_urls ) ) as progress_bar:
    with ThreadPoolExecutor() as executor:
        futures = []
        for url in found_media_urls:
            futures.append( executor.submit( download_media_file, storage_path, url ) )
        
        for future in as_completed( futures ):
            progress_bar.update( 1 )

print( "All downloads are now complete!" )