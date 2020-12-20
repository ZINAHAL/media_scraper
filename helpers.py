import re
import os
import requests
from bs4 import BeautifulSoup


def create_directory_to_store_media():
    directory_name = input( "Enter a name for the folder: " )
    path = os.getcwd() + '/' + directory_name
    try:
        os.mkdir( path )
    except FileExistsError:
        print( f"A folder with the name -- {directory_name} -- already exsists. Please try again and provide a different name." )
        return None
    else:
        print( f"Successfuly created a folder with the name: {directory_name}" )
        return path


# if found, [ ./ , / ] are removed from the beginning of path
def clean_path( path ):
    match_object = re.search( r'^(\.)*(/)+', path )
    if match_object is None:
        return path
    return re.sub( match_object.group(), '', path, 1 )


def get_media_paths( url ):
    if url is None:
        return []
    regx_pattern = re.compile( r'(.gif|.jpg.png|.png|.jpg|.jpeg|.docx|.pdf|.mp3|.mp4)\b', re.IGNORECASE )
    html_content = requests.get( url ).text
    soup = BeautifulSoup( html_content, 'html.parser' )
    href_paths = [ tag['href'] for tag in soup( href=regx_pattern ) ]
    src_paths = [ tag['src'] for tag in soup( src=regx_pattern ) ]
    return href_paths + src_paths


def get_all_hrefs( url, origin ):
    html_content = requests.get( url ).text
    soup = BeautifulSoup( html_content, 'html.parser' )
    a_tags = soup.find_all( 'a', attrs={ 'href': re.compile( origin ) } )
    return [ a['href'] for a in a_tags ]


def download_media_file( storage_path, url ):
    with requests.get( url, stream=True ) as response:
        with open( storage_path + '/' + url.rsplit( '/', 1 )[1], 'wb' ) as location:
            for chunk in response.iter_content( chunk_size=1024*140 ):
                if chunk:
                    location.write( chunk )
    