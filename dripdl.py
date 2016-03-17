#! /usr/bin/python

import requests
import json

username = raw_input("Drip email: ")
password = raw_input("Drip password: ")

filetype = raw_input("What filetype do you want to download?: ")

payload = {
    'email': username,
    'password': password
}

def getRelease(filename, url, s):
    print "Download url: " + url
    d = s.get(url, stream=True)
    print d.status_code
    if d.status_code == 200:
        print "Saving: " + filename
        with open(filename, 'wb') as f:
            for chunk in d.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        print "File Saved!\n"
    else:
        print "Error downloading: " + filename

    return d.status_code

with requests.Session() as s:
    p = s.post('https://drip.com/api/users/login', data=payload)
    if p.status_code != 201:
        raw_input("Error logging in")
        exit()
    page = 1
    
    while True:
        r = s.get('https://drip.com/api/users/20251/releases?page=' + str(page))
        releases = r.json()
        if not releases:
            print "Done downloading releases"
            break
        for release in releases:
            print release[u'title']
            baseurl = 'https://drip.com/api/creatives/' + str(release[u'creative_id']) + '/releases/' + str(release[u'id'])
            valid_types = s.get(baseurl + '/formats')
            success = getRelease(release[u'slug'] + "[" + filetype + "].zip", baseurl + '/download?release_format=' + filetype, s)
            if success != 200:
                print "Unable to download file"
                print "Available filetypes are: " + valid_types.text
                new_filetype = raw_input("Do you want to download a different filetype?: ")
                if new_filetype != "no":
                     getRelease(release[u'slug'] + "[" + new_filetype + "].zip", baseurl + '/download?release_format=' + new_filetype, s)
        page += 1
