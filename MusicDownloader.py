#!/usr/bin/env python
# coding=utf-8
import json
import random
import string
import sys
import time
import urllib
import urllib2
song_list_file = 'DownloadMusicList.txt'
file_obj = open(song_list_file, 'r')
if_first_song = True
for eachline in file_obj:
    if if_first_song:
        if_first_song = False
    else:
        print "Now waiting for another download..."
        print "-"*20
        time.sleep(5)
    song_name =  eachline.strip()
    print "{} download started...".format(song_name)

    # Find the song_id with the given song name:
    #
    kwurl = "http://search.kuwo.cn/r.s?all={}&ft=music&client=kt&cluster=0&rn=10&rformat=json&callback=searchMusicResult&encoding=utf8&vipver=MUSIC_8.0.3.1&".format(urllib.quote(song_name))
    search_result_json = urllib2.urlopen(kwurl).read()[19:-52]
    try:
        search_result = json.loads(search_result_json.replace('\'','"'))
    except:
        print >> sys.stderr, "Unable to parse json str."
        with open('search_result.json','w') as f:
            f.write(search_result_json)
    l = search_result['abslist']
    song_id = l[0]['MUSICRID'][6:]
    print "Song id acquired."

    # Find the mp3 url with given song_id:
    #
    rand_num_str = ''.join(random.choice(string.digits) for _ in range(13))
    request = urllib2.Request('http://www.170hi.com/tool/song/ajax/api.php?callback=callback&kwId={}&_={}'.format(song_id, rand_num_str))
    # print "got the request"
    request.add_header('Referer', 'http://www.170mv.com/tool/song/?song={}'.format(song_id))
    try:
            response=urllib2.urlopen(request)
    except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
            print "The server couldn't fulfill the request"
            print "Error code:",e.code
            print "Return content:",e.read()
    except urllib2.URLError,e:
            print "Failed to reach the server"
            print "The reason:",e.reason
    # response = urllib2.urlopen(request)
    # print "got the response."
    search_result_json = response.read()[9:-1]
    # print search_result_json
    mp3_url = json.loads(search_result_json)["hdVideoUrl"]
    print "mp3 url acquired."

    # Download and name module:
    # download the file with given mp3 url
    #
    print "Downloading the file..."
    response = urllib2.urlopen(mp3_url)
    data = response.read()
    file = open("./music/{}.mp3".format(song_name),'w')
    file.write(data)
    file.close()
    print "{} download completed.".format(song_name)
