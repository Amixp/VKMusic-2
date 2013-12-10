import urllib
import config
import http.cookiejar
import datetime
import os
import json
import time
import song
import flag

def loadsongs(cfg, songlist, flg):
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),
        urllib.request.HTTPRedirectHandler())
    params = dict()
    params["owner_id"] = cfg.user_id
    params["need_user"] = 0
    params["offset"] = 0
    params["count"] = 6000
    params["access_token"] = cfg.access_token
    par_list = []
    for name in params:
        par_list.append(name + "=" + str(params[name]))
    params = "&".join(par_list)
    update_time = datetime.datetime.now()
    while True:
        if datetime.datetime.now() > cfg.expires_in:
            cfg.updateconfig()
        while datetime.datetime.now() < update_time:
            time.sleep(30)
        delta = datetime.timedelta(0,0,0,0,cfg.interval,0,0)
        update_time += delta
        print("Load tracklist")
        url = 'https://api.vk.com/method/audio.get?' + params
        response = opener.open(url)
        response = response.read()
        response = response.decode("UTF-8")
        response = response.replace('\/','/')
        response = response.replace('&amp;','&')
        response = json.loads(response)
        songs = []
        print("loaded")
        songlist.clear()
        flg.songlist = False
        for i in response:
            for song_info in response[i]:
                if isinstance(song_info,dict):
                    some = song.song(song_info)
                    songs.append(some)
                    songlist.append(some)
        flg.songlist = True
        if not os.path.isdir(cfg.path):
            os.makedirs(cfg.path)
        skipped = 0
        with open('skipped.dat', 'w') as f:
            f.write('')
        for sng in songs:
            sng.do_replacement(cfg.replacement)
            t_path = cfg.path + sng.artist + " - " + sng.title + '.mp3'
            if os.path.exists(t_path) and os.path.getsize(t_path) != 0:
                skipped += 1
                with open('skipped.dat', 'ab') as f:
                    f.write((t_path + ' skipped\n').encode("UTF-8"))
            else:
                print('Downloading ' + t_path)
                with open(t_path, 'wb') as f:
                    response = opener.open(sng.url)
                    response = response.read()
                    f.write(response)
                print('ready')
        word = ' songs'
        if skipped == 1:
            word = ' song'
        print('Skipped ' + str(skipped) + word + '. More info in skipped.dat, you can open it as txt file.')
        print('Next update in ' + str(update_time))
